from flask import Blueprint
from controllers.tracking_controller import track_order
from flask_jwt_extended import jwt_required

tracking_bp = Blueprint('tracking', __name__)

tracking_bp.route('/<int:order_id>', methods=['GET'])(jwt_required()(track_order))
