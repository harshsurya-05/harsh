from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user_model import User


@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200


@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # --- Common updatable fields ---
    str_fields = ['name', 'phone', 'address', 'profile_photo', 'preferred_language', 'notification_prefs']
    for f in str_fields:
        if f in data and data[f] is not None:
            val = data[f].strip() if isinstance(data[f], str) else data[f]
            if f == 'name' and not val:
                continue
            setattr(user, f, val)

    if 'gps_lat' in data:
        user.gps_lat = data['gps_lat']
    if 'gps_lng' in data:
        user.gps_lng = data['gps_lng']

    # --- Farmer fields ---
    if user.role == 'farmer':
        for f in ['farm_location', 'farming_type', 'crops_category', 'quantity_available', 'upi_id', 'bank_account']:
            if f in data:
                setattr(user, f, data[f])

    # --- Customer fields ---
    elif user.role == 'customer':
        if 'delivery_addresses' in data:
            user.delivery_addresses = data['delivery_addresses']
        if 'payment_method' in data:
            user.payment_method = data['payment_method']

    # --- Delivery Boy fields ---
    elif user.role == 'delivery':
        for f in ['vehicle_type', 'license_number']:
            if f in data:
                setattr(user, f, data[f])
        if 'availability_status' in data and data['availability_status'] in ('online', 'offline'):
            user.availability_status = data['availability_status']

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200


@jwt_required()
def rate_user():
    """Rate a farmer or delivery boy."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    target_id = data.get('user_id')
    stars = data.get('rating')

    if not target_id or stars is None:
        return jsonify({'error': 'user_id and rating are required'}), 400
    if not (1 <= float(stars) <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    if str(target_id) == str(current_user_id):
        return jsonify({'error': 'Cannot rate yourself'}), 400

    target = db.session.get(User, target_id)
    if not target:
        return jsonify({'error': 'User not found'}), 404

    # Weighted average
    total = target.rating * target.rating_count + float(stars)
    target.rating_count += 1
    target.rating = round(total / target.rating_count, 1)
    db.session.commit()

    return jsonify({'message': 'Rating submitted', 'new_rating': target.rating}), 200
