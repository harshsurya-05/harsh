from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from models.order_model import Order
from models.delivery_model import Delivery
from services.map_service import simulate_movement


def track_order(order_id):
    customer_id = int(get_jwt_identity())
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    if order.customer_id != customer_id:
        return jsonify({'error': 'Unauthorized'}), 403

    delivery = Delivery.query.filter_by(order_id=order_id).first()
    if not delivery:
        return jsonify({'error': 'No delivery record found'}), 404

    # Simulate GPS movement for demo
    new_lat, new_lng = simulate_movement(delivery.current_lat, delivery.current_lng)
    delivery.current_lat = new_lat
    delivery.current_lng = new_lng
    db.session.commit()

    status_steps = ['preparing', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered']
    current_index = status_steps.index(delivery.status) if delivery.status in status_steps else 0

    return jsonify({
        'order_id': order.id,
        'order_status': order.status,
        'delivery': delivery.to_dict(),
        'tracking': {
            'current_step': current_index,
            'total_steps': len(status_steps),
            'steps': [
                {'key': 'preparing', 'label': 'Order Preparing', 'icon': '📦'},
                {'key': 'picked_up', 'label': 'Picked Up', 'icon': '🚜'},
                {'key': 'in_transit', 'label': 'In Transit', 'icon': '🚚'},
                {'key': 'out_for_delivery', 'label': 'Out for Delivery', 'icon': '🏃'},
                {'key': 'delivered', 'label': 'Delivered', 'icon': '✅'},
            ]
        }
    }), 200
