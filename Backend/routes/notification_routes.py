from flask import Blueprint
from controllers.notification_controller import get_my_notifications, mark_as_read, delete_notification
from flask_jwt_extended import jwt_required

notification_bp = Blueprint('notifications', __name__)

notification_bp.route('/', methods=['GET'])(jwt_required()(get_my_notifications))
notification_bp.route('/<int:notif_id>/read', methods=['PUT'])(jwt_required()(mark_as_read))
notification_bp.route('/<int:notif_id>', methods=['DELETE'])(jwt_required()(delete_notification))
