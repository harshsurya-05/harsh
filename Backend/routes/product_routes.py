from flask import Blueprint
from controllers.product_controller import (
    get_products, create_product, update_product, 
    delete_product, ai_price_suggestion, record_activity
)
from middleware.auth_middleware import farmer_required

from flask_jwt_extended import jwt_required

product_bp = Blueprint('products', __name__)

product_bp.route('/', methods=['GET'])(get_products)
product_bp.route('/', methods=['POST'])(farmer_required(create_product))
product_bp.route('/<int:product_id>', methods=['PUT'])(farmer_required(update_product))
product_bp.route('/<int:product_id>', methods=['DELETE'])(farmer_required(delete_product))
product_bp.route('/ai-price', methods=['GET'])(ai_price_suggestion)
product_bp.route('/activity', methods=['POST'])(jwt_required()(record_activity))
