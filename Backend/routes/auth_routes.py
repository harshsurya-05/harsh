from flask import Blueprint
from controllers.auth_controller import (
    register, login, get_profile, update_profile,
    refresh, forgot_password, reset_password, get_nearby_farmers
)
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

# Auth
auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/refresh', methods=['POST'])(refresh)
auth_bp.route('/forgot-password', methods=['POST'])(forgot_password)
auth_bp.route('/reset-password', methods=['POST'])(reset_password)

# Profile
auth_bp.route('/profile', methods=['GET'])(jwt_required()(get_profile))
auth_bp.route('/profile', methods=['PUT'])(jwt_required()(update_profile))
auth_bp.route('/farmers/nearby', methods=['GET'])(jwt_required()(get_nearby_farmers))
