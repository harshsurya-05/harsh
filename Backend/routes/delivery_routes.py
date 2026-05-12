from flask import Blueprint
from controllers.delivery_controller import (
    get_delivery, update_delivery_status,
    get_farmer_deliveries, get_customer_deliveries
)
from flask_jwt_extended import jwt_required

delivery_bp = Blueprint('delivery', __name__)

delivery_bp.route('/order/<int:order_id>', methods=['GET'])(jwt_required()(get_delivery))
delivery_bp.route('/order/<int:order_id>/status', methods=['PUT'])(jwt_required()(update_delivery_status))
delivery_bp.route('/farmer', methods=['GET'])(jwt_required()(get_farmer_deliveries))
delivery_bp.route('/customer', methods=['GET'])(jwt_required()(get_customer_deliveries))
