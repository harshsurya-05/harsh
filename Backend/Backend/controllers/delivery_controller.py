from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from models.delivery_model import Delivery
from models.order_model import Order
import random


def get_delivery(order_id):
    """Get delivery info for an order."""
    delivery = Delivery.query.filter_by(order_id=order_id).first()
    if not delivery:
        return jsonify({'error': 'Delivery not found for this order'}), 404
    return jsonify({'delivery': delivery.to_dict()}), 200


def update_delivery_status(order_id):
    """Farmer or delivery agent updates delivery status."""
    data = request.get_json()
    new_status = data.get('status', '').strip().lower()

    valid = ['preparing', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'failed', 'cancelled']
    if new_status not in valid:
        return jsonify({'error': f'Invalid status. Choose from: {", ".join(valid)}'}), 400

    delivery = Delivery.query.filter_by(order_id=order_id).first()
    if not delivery:
        return jsonify({'error': 'Delivery not found'}), 404

    delivery.status = new_status

    # Update parent order status too
    if new_status == 'delivered':
        if delivery.order:
            delivery.order.status = 'delivered'

    # Optionally update GPS coords
    if 'lat' in data and 'lng' in data:
        delivery.current_lat = data['lat']
        delivery.current_lng = data['lng']

    db.session.commit()
    return jsonify({'message': f'Delivery status updated to {new_status}', 'delivery': delivery.to_dict()}), 200


def get_farmer_deliveries():
    """Get all deliveries for orders that belong to this farmer."""
    farmer_id = int(get_jwt_identity())
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    result = []
    for order in all_orders:
        if any(i.get('farmer_id') == farmer_id for i in order.items):
            if order.delivery:
                d = order.delivery.to_dict()
                d['order_status'] = order.status
                d['customer_name'] = order.customer.name if order.customer else 'Customer'
                result.append(d)
    return jsonify({'deliveries': result}), 200


def get_customer_deliveries():
    """Get all active deliveries for the logged-in customer."""
    customer_id = int(get_jwt_identity())
    orders = Order.query.filter_by(customer_id=customer_id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        if order.delivery:
            d = order.delivery.to_dict()
            d['order_status'] = order.status
            d['items'] = order.items
            d['total_amount'] = order.total_amount
            result.append(d)
    return jsonify({'deliveries': result}), 200
