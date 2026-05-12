from flask import Blueprint
from controllers.admin_controller import get_admin_stats, get_all_users, toggle_user_status, get_all_orders
from middleware.auth_middleware import admin_required

admin_bp = Blueprint('admin', __name__)

# Apply admin_required middleware to all routes in this blueprint
@admin_bp.before_request
@admin_required
def before_admin_request():
    pass

admin_bp.route('/stats', methods=['GET'])(get_admin_stats)
admin_bp.route('/users', methods=['GET'])(get_all_users)
admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])(toggle_user_status)
admin_bp.route('/orders', methods=['GET'])(get_all_orders)
