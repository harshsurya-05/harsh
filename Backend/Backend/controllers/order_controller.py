from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps
from app import db
from models.order_model import Order
from models.product_model import Product
from models.user_model import User
from models.delivery_model import Delivery
from services.payment_service import process_payment
from services.map_service import get_initial_coordinates
from utils.helpers import validate_required_fields
from controllers.notification_controller import create_notification
from datetime import datetime, timedelta
import uuid


def create_order():
    data = request.get_json()
    customer_id = int(get_jwt_identity())

    missing = validate_required_fields(data, ['items', 'delivery_address', 'payment_method'])
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    items = data['items']
    if not items:
        return jsonify({'error': 'Order must have at least one item'}), 400

    order_items = []
    total = 0.0
    for item in items:
        product = db.session.get(Product, item['product_id'])
        if not product or not product.is_active:
            return jsonify({'error': f'Product {item["product_id"]} not found'}), 404
        if product.stock < item['qty']:
            return jsonify({'error': f'Insufficient stock for {product.name}'}), 400

        subtotal = product.price * item['qty']
        total += subtotal
        order_items.append({
            'product_id': product.id,
            'farmer_id': product.farmer_id,
            'name': product.name,
            'price': product.price,
            'qty': item['qty'],
            'unit': product.unit,
            'subtotal': subtotal
        })
        product.stock -= item['qty']

    order = Order(
        customer_id=customer_id,
        total_amount=round(total, 2),
        status='confirmed',
        delivery_address=data['delivery_address'],
        payment_status='unpaid'
    )
    order.items = order_items
    db.session.add(order)
    db.session.flush()

    payment_result = process_payment(order.id, total, data['payment_method'])
    if payment_result['success']:
        order.payment_status = 'paid'
        order.payment_id = payment_result['transaction_id']
        order.status = 'processing'

    lat, lng = get_initial_coordinates()
    delivery = Delivery(
        order_id=order.id,
        delivery_address=data['delivery_address'],
        status='preparing',
        courier_name='AgroHub Express',
        tracking_number=f'AH{order.id:06d}{uuid.uuid4().hex[:4].upper()}',
        current_lat=lat,
        current_lng=lng,
        estimated_delivery=datetime.utcnow() + timedelta(days=3)
    )
    db.session.add(delivery)
    db.session.commit()

    # Trigger Notifications for Farmers
    unique_farmer_ids = {item['farmer_id'] for item in order_items}
    customer = db.session.get(User, customer_id)
    customer_name = customer.name if customer else "A customer"

    for f_id in unique_farmer_ids:
        farmer_items = [i for i in order_items if i['farmer_id'] == f_id]
        farmer_total = sum(i['subtotal'] for i in farmer_items)
        items_desc = ", ".join([f"{i['qty']} {i['unit']} {i['name']}" for i in farmer_items])

        create_notification(
            user_id=f_id,
            title="New Order Received! 📦 (नया ऑर्डर मिला!)",
            message=f"{customer_name} ordered {items_desc}. Total: ₹{farmer_total:.2f}. ( {customer_name} ने {items_desc} का ऑर्डर दिया है। कुल: ₹{farmer_total:.2f} )",
            n_type="success"
        )
        
        # Simulate SMS/Email Notification
        print(f"DEBUG: Sending SMS/Email to Farmer (ID: {f_id}): New order from {customer_name} for ₹{farmer_total:.2f}")

    return jsonify({
        'message': 'Order placed successfully',
        'order': order.to_dict(),
        'delivery': delivery.to_dict(),
        'payment': payment_result
    }), 201


def get_order(order_id):
    customer_id = int(get_jwt_identity())
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    if order.customer_id != customer_id:
        return jsonify({'error': 'Unauthorized'}), 403

    result = order.to_dict()
    if order.delivery:
        result['delivery'] = order.delivery.to_dict()
    return jsonify({'order': result}), 200


def get_customer_orders():
    customer_id = int(get_jwt_identity())
    orders = Order.query.filter_by(customer_id=customer_id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        o_dict = order.to_dict()
        if order.delivery:
            o_dict['delivery'] = order.delivery.to_dict()
        result.append(o_dict)
    return jsonify({'orders': result}), 200


def get_farmer_orders():
    farmer_id = int(get_jwt_identity())
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    farmer_orders = []

    for order in all_orders:
        farmer_items = [item for item in order.items if item.get('farmer_id') == farmer_id]
        if farmer_items:
            o_dict = order.to_dict()
            o_dict['items'] = farmer_items
            o_dict['farmer_total'] = sum(item['subtotal'] for item in farmer_items)
            if order.delivery:
                o_dict['delivery'] = order.delivery.to_dict()
            farmer_orders.append(o_dict)

    return jsonify({'orders': farmer_orders}), 200


def update_order_status(order_id):
    """Farmer or admin can update order status."""
    data = request.get_json()
    new_status = data.get('status', '').strip().lower()

    valid_statuses = ['pending', 'confirmed', 'processing', 'accepted',
                      'rejected', 'shipped', 'in_transit', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400

    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    order.status = new_status
    order.updated_at = datetime.utcnow()

    # Also update delivery status in sync
    if order.delivery:
        if new_status == 'shipped':
            order.delivery.status = 'in_transit'
        elif new_status == 'delivered':
            order.delivery.status = 'delivered'
        elif new_status in ('cancelled', 'rejected'):
            order.delivery.status = 'cancelled'

    db.session.commit()

    # Notify Customer
    create_notification(
        user_id=order.customer_id,
        title=f"Order Update: {new_status.capitalize()} 📦",
        message=f"Your order # {order.id} status has been updated to {new_status}.",
        n_type="info"
    )

    result = order.to_dict()
    if order.delivery:
        result['delivery'] = order.delivery.to_dict()
    return jsonify({'message': f'Order status updated to {new_status}', 'order': result}), 200


def cancel_order(order_id):
    """Customer cancels their own order."""
    customer_id = int(get_jwt_identity())
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    if order.customer_id != customer_id:
        return jsonify({'error': 'Unauthorized'}), 403
    if order.status in ('delivered', 'shipped', 'in_transit'):
        return jsonify({'error': 'Cannot cancel order that is already shipped or delivered'}), 400

    order.status = 'cancelled'
    order.updated_at = datetime.utcnow()

    # Restore stock
    for item in order.items:
        product = db.session.get(Product, item['product_id'])
        if product:
            product.stock += item['qty']

    if order.delivery:
        order.delivery.status = 'cancelled'

    db.session.commit()
    return jsonify({'message': 'Order cancelled successfully'}), 200


def get_farmer_stats():
    """Returns summary stats for farmer dashboard."""
    farmer_id = int(get_jwt_identity())

    # Products
    products = Product.query.filter_by(farmer_id=farmer_id, is_active=True).all()
    total_products = len(products)
    low_stock = [p.to_dict() for p in products if p.stock < 20]
    out_of_stock = [p.to_dict() for p in products if p.stock <= 0]

    # Orders
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    farmer_orders = []
    total_earnings = 0.0
    pending_count = 0

    for order in all_orders:
        farmer_items = [item for item in order.items if item.get('farmer_id') == farmer_id]
        if farmer_items:
            subtotal = sum(item['subtotal'] for item in farmer_items)
            total_earnings += subtotal
            if order.status in ('pending', 'confirmed', 'processing'):
                pending_count += 1
            farmer_orders.append(order)

    # Monthly Sales for Charts
    monthly_sales = {}
    for o in farmer_orders:
        month = o.created_at.strftime('%b')
        farmer_items = [item for item in o.items if item.get('farmer_id') == farmer_id]
        subtotal = sum(item['subtotal'] for item in farmer_items)
        monthly_sales[month] = monthly_sales.get(month, 0) + subtotal

    return jsonify({
        'total_orders': len(farmer_orders),
        'total_earnings': round(total_earnings, 2),
        'pending_orders': pending_count,
        'total_products': total_products,
        'low_stock_products': low_stock,
        'out_of_stock_products': out_of_stock,
        'chart_data': {
            'labels': list(monthly_sales.keys()),
            'values': list(monthly_sales.values())
        }
    }), 200


def get_customer_stats():
    """Returns summary stats for customer dashboard."""
    customer_id = int(get_jwt_identity())
    orders = Order.query.filter_by(customer_id=customer_id).all()
    total_orders = len(orders)
    active_deliveries = sum(1 for o in orders if o.status not in ('delivered', 'cancelled', 'rejected'))
    total_spent = sum(o.total_amount for o in orders if o.payment_status == 'paid')

    return jsonify({
        'total_orders': total_orders,
        'active_deliveries': active_deliveries,
        'total_spent': round(total_spent, 2)
    }), 200


def get_payment_history():
    """Returns payment history for the logged-in user."""
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    role = claims.get('role')

    if role == 'customer':
        orders = Order.query.filter_by(customer_id=user_id).order_by(Order.created_at.desc()).all()
    else:
        # Farmer: return orders where they have items
        all_orders = Order.query.order_by(Order.created_at.desc()).all()
        orders = [o for o in all_orders if any(i.get('farmer_id') == user_id for i in o.items)]

    result = []
    for o in orders:
        result.append({
            'order_id': o.id,
            'date': o.created_at.strftime('%d %b %Y'),
            'amount': o.total_amount,
            'payment_status': o.payment_status,
            'payment_id': o.payment_id,
            'order_status': o.status
        })

    return jsonify({'payments': result}), 200

from flask import send_file
from services.invoice_service import generate_invoice_pdf

def download_invoice(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    pdf_buffer = generate_invoice_pdf(order)
    return send_file(pdf_buffer, as_attachment=True, download_name=f'AgroHub_Invoice_{order_id}.pdf', mimetype='application/pdf')
