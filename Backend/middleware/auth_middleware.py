from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def farmer_required(fn):
    """Decorator: requires valid JWT with role=farmer."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'detail': str(e)}), 401

        claims = get_jwt()
        if claims.get('role') != 'farmer':
            return jsonify({'error': 'Farmer access required'}), 403

        return fn(*args, **kwargs)
    return wrapper


def customer_required(fn):
    """Decorator: requires valid JWT with role=customer."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'detail': str(e)}), 401

        claims = get_jwt()
        if claims.get('role') != 'customer':
            return jsonify({'error': 'Customer access required'}), 403

        return fn(*args, **kwargs)
    return wrapper


def delivery_required(fn):
    """Decorator: requires valid JWT with role=delivery."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'detail': str(e)}), 401

        claims = get_jwt()
        if claims.get('role') != 'delivery':
            return jsonify({'error': 'Delivery access required'}), 403

        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """Decorator: requires valid JWT with role=admin."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'detail': str(e)}), 401

        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return fn(*args, **kwargs)
    return wrapper
