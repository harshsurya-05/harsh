from flask import Blueprint
from controllers.order_controller import (
    create_order, get_order, get_customer_orders, get_farmer_orders,
    update_order_status, cancel_order,
    get_farmer_stats, get_customer_stats, get_payment_history,
    download_invoice
)
from flask_jwt_extended import jwt_required

order_bp = Blueprint('orders', __name__)

# Core order APIs
order_bp.route('/', methods=['POST'])(jwt_required()(create_order))
order_bp.route('/<int:order_id>', methods=['GET'])(jwt_required()(get_order))
order_bp.route('/customer', methods=['GET'])(jwt_required()(get_customer_orders))
order_bp.route('/farmer', methods=['GET'])(jwt_required()(get_farmer_orders))

# Status update & cancel
order_bp.route('/<int:order_id>/status', methods=['PUT'])(jwt_required()(update_order_status))
order_bp.route('/<int:order_id>/cancel', methods=['PUT'])(jwt_required()(cancel_order))

# Dashboard stats
order_bp.route('/stats/farmer', methods=['GET'])(jwt_required()(get_farmer_stats))
order_bp.route('/stats/customer', methods=['GET'])(jwt_required()(get_customer_stats))

# Payment history
order_bp.route('/payments/history', methods=['GET'])(jwt_required()(get_payment_history))
