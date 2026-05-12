from flask import request, jsonify
from app import db
from models.user_model import User
from models.order_model import Order
from models.product_model import Product
from sqlalchemy import func

def get_admin_stats():
    """Returns overall platform stats for the admin."""
    total_users = User.query.count()
    total_farmers = User.query.filter_by(role='farmer').count()
    total_customers = User.query.filter_by(role='customer').count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0.0
    total_products = Product.query.count()

    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_farmers': total_farmers,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'total_products': total_products
        }
    }), 200

def get_all_users():
    """Returns a list of all users."""
    users = User.query.all()
    return jsonify({'users': [u.to_dict() for u in users]}), 200

def toggle_user_status(user_id):
    """Deactivate/Activate a user account."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({
        'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
        'is_active': user.is_active
    }), 200

def get_all_orders():
    """Returns all orders on the platform."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({'orders': [o.to_dict() for o in orders]}), 200
