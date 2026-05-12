from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from models.notification_model import Notification

def get_my_notifications():
    user_id = int(get_jwt_identity())
    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(20).all()
    return jsonify({'notifications': [n.to_dict() for n in notifs]}), 200

def mark_as_read(notif_id):
    user_id = int(get_jwt_identity())
    notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
    if notif:
        notif.is_read = True
        db.session.commit()
    return jsonify({'message': 'Marked as read'}), 200

def delete_notification(notif_id):
    user_id = int(get_jwt_identity())
    notif = Notification.query.filter_by(id=notif_id, user_id=user_id).first()
    if notif:
        db.session.delete(notif)
        db.session.commit()
    return jsonify({'message': 'Deleted'}), 200

def create_notification(user_id, title, message, n_type='info'):
    """Utility function to create a notification (internal use)."""
    notif = Notification(user_id=user_id, title=title, message=message, type=n_type)
    db.session.add(notif)
    db.session.commit()
    return notif
