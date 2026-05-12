from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    get_jwt_identity, jwt_required, get_jwt
)
from app import db, mail
from flask_mail import Message
from models.user_model import User
from utils.helpers import validate_email, validate_required_fields
import uuid
import datetime


def _generate_referral_code():
    while True:
        code = 'AH' + uuid.uuid4().hex[:6].upper()
        if not User.query.filter_by(referral_code=code).first():
            return code


def register():
    data = request.get_json()
    missing = validate_required_fields(data, ['name', 'email', 'password', 'role'])
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    if data['role'] not in ('farmer', 'customer', 'delivery', 'admin'):
        return jsonify({'error': 'Invalid role'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email address'}), 400

    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify({'error': 'Email already registered'}), 409

    referred_by = None
    if data.get('referral_code'):
        referring_user = User.query.filter_by(referral_code=data['referral_code'].upper()).first()
        if not referring_user:
            return jsonify({'error': 'Invalid referral code'}), 400
        referred_by = data['referral_code'].upper()

    user = User(
        name=data['name'].strip(),
        email=data['email'].lower().strip(),
        password_hash=generate_password_hash(data['password']),
        role=data['role'],
        phone=data.get('phone'),
        address=data.get('address'),
        profile_photo=data.get('profile_photo'),
        preferred_language=data.get('preferred_language', 'english'),
        referral_code=_generate_referral_code(),
        referred_by=referred_by,
        gps_lat=data.get('gps_lat'),
        gps_lng=data.get('gps_lng'),
        notification_prefs=data.get('notification_prefs', 'email,sms'),
    )

    if data['role'] == 'farmer':
        user.farm_location   = data.get('farm_location')
        user.farming_type    = data.get('farming_type', 'Regular')
        user.crops_category  = data.get('crops_category')
        user.quantity_available = data.get('quantity_available')
        user.upi_id          = data.get('upi_id')
        user.bank_account    = data.get('bank_account')
    elif data['role'] == 'customer':
        user.delivery_addresses = data.get('delivery_addresses')
        user.payment_method     = data.get('payment_method', 'cod')
    elif data['role'] == 'delivery':
        user.vehicle_type         = data.get('vehicle_type')
        user.license_number       = data.get('license_number')
        user.availability_status  = 'offline'

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Registration successful', 
        'access_token': access_token, 
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 201


def login():
    data = request.get_json()
    missing = validate_required_fields(data, ['email', 'password'])
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    user = User.query.filter_by(email=data['email'].lower().strip()).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Your account has been deactivated'}), 403

    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful', 
        'access_token': access_token, 
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity))
    access_token = create_access_token(identity=identity, additional_claims={'role': user.role if user else 'user'})
    return jsonify({'access_token': access_token}), 200


def forgot_password():
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # For security, don't reveal if user exists
        return jsonify({'message': 'If your email is registered, you will receive a reset link.'}), 200

    token = uuid.uuid4().hex
    user.reset_token = token
    user.reset_token_expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    db.session.commit()

    # Send Email (Placeholder logic if Mail not configured)
    try:
        reset_link = f"http://localhost:5500/Frontend/html/reset-password.html?token={token}"
        msg = Message("AgroHub — Password Reset Request",
                      recipients=[user.email])
        msg.body = f"Hello {user.name},\n\nYou requested a password reset. Click the link below to reset it:\n{reset_link}\n\nThis link expires in 1 hour."
        mail.send(msg)
    except Exception as e:
        print(f"Mail Error: {e}")
        return jsonify({'message': 'If your email is registered, you will receive a reset link.', 'debug_token': token}), 200

    return jsonify({'message': 'If your email is registered, you will receive a reset link.'}), 200


def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return jsonify({'error': 'Token and password are required'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.datetime.utcnow():
        return jsonify({'error': 'Invalid or expired token'}), 400

    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({'message': 'Password reset successful. You can now login.'}), 200


def get_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200


def update_profile():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    for field in ['name', 'phone', 'address', 'preferred_language',
                  'profile_photo', 'gps_lat', 'gps_lng', 'notification_prefs']:
        if field in data:
            setattr(user, field, data[field])

    if user.role == 'farmer':
        for field in ['farm_location', 'farming_type', 'crops_category',
                      'quantity_available', 'upi_id', 'bank_account']:
            if field in data:
                setattr(user, field, data[field])

    if user.role == 'customer':
        for field in ['delivery_addresses', 'payment_method']:
            if field in data:
                setattr(user, field, data[field])

    if user.role == 'delivery':
        for field in ['vehicle_type', 'availability_status']:
            if field in data:
                setattr(user, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'user': user.to_dict()}), 200


def get_nearby_farmers():
    """Returns a list of farmers. In a real app, this would use GPS coordinates."""
    farmers = User.query.filter_by(role='farmer', is_active=True).limit(10).all()
    return jsonify({'farmers': [f.to_dict() for f in farmers]}), 200

