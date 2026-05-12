from flask import Blueprint
from controllers.review_controller import submit_review, get_product_reviews, get_my_reviews
from flask_jwt_extended import jwt_required

review_bp = Blueprint('reviews', __name__)

review_bp.route('/', methods=['POST'])(jwt_required()(submit_review))
review_bp.route('/product/<int:product_id>', methods=['GET'])(get_product_reviews)
review_bp.route('/mine', methods=['GET'])(jwt_required()(get_my_reviews))
