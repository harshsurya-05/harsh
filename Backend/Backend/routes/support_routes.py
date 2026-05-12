from flask import Blueprint
from controllers.support_controller import send_support_message
from flask_jwt_extended import jwt_required

support_bp = Blueprint('support', __name__)

support_bp.route('/chat', methods=['POST'])(jwt_required()(send_support_message))
