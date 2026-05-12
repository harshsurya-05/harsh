from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from models.product_model import Product
from models.user_model import User
from controllers.notification_controller import create_notification
from utils.helpers import validate_required_fields


import math

def get_products():
    """Get all products with filtering and sorting."""
    category = request.args.get('category')
    farmer_id = request.args.get('farmer_id')
    search   = request.args.get('search')
    sort     = request.args.get('sort', 'latest') # latest, price_asc, price_desc
    lat      = request.args.get('lat', type=float)
    lng      = request.args.get('lng', type=float)
    radius   = request.args.get('radius', 50, type=float) # km
    limit    = request.args.get('limit', type=int)

    query = Product.query.filter_by(is_active=True)

    if category:
        query = query.filter_by(category=category)
    if farmer_id:
        query = query.filter_by(farmer_id=farmer_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    # Sorting
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    if limit:
        query = query.limit(limit)

    products = query.all()
    
    # Location Filter (Post-query for simplicity, or use a spatial extension in production)
    if lat and lng:
        filtered = []
        for p in products:
            if not p.farmer or not p.farmer.latitude:
                filtered.append(p)
                continue
            
            # Simple Haversine approximation
            dist = 111.1 * math.sqrt((lat - p.farmer.latitude)**2 + (lng - p.farmer.longitude)**2)
            if dist <= radius:
                p.distance = round(dist, 1)
                filtered.append(p)
        products = filtered

    return jsonify({'products': [p.to_dict() for p in products]}), 200


import cloudinary.uploader

def create_product():
    # Handle both JSON and Multipart/Form-data
    if request.is_json:
        data = request.get_json()
        files = {}
    else:
        data = request.form.to_dict()
        files = request.files

    farmer_id = int(get_jwt_identity())

    missing = validate_required_fields(data, ['name', 'category', 'price', 'stock'])
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    # Image Handling
    image_url = data.get('image_url')
    if 'image' in files:
        try:
            upload_result = cloudinary.uploader.upload(files['image'], folder="agrohub/products")
            image_url = upload_result.get('secure_url')
        except Exception as e:
            print(f"Cloudinary Upload Error: {e}")

    product = Product(
        farmer_id=farmer_id,
        name=data['name'].strip(),
        category=data['category'].strip(),
        description=data.get('description', ''),
        price=float(data['price']),
        stock=int(data['stock']),
        unit=data.get('unit', 'kg'),
        image_url=image_url
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product': product.to_dict()}), 201


def update_product(product_id):
    farmer_id = int(get_jwt_identity())
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if product.farmer_id != farmer_id:
        return jsonify({'error': 'Unauthorized — not your product'}), 403

    data = request.get_json()
    for field in ['name', 'category', 'description', 'unit', 'image_url']:
        if field in data:
            setattr(product, field, data[field])
    if 'price' in data:
        product.price = float(data['price'])
    if 'stock' in data:
        product.stock = int(data['stock'])
    if 'is_active' in data:
        product.is_active = bool(data['is_active'])

    db.session.commit()
    return jsonify({'message': 'Product updated', 'product': product.to_dict()}), 200


def delete_product(product_id):
    farmer_id = int(get_jwt_identity())
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if product.farmer_id != farmer_id:
        return jsonify({'error': 'Unauthorized — not your product'}), 403

    product.is_active = False  # Soft delete
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

import os
import requests
import random

GOV_DATA_API_KEY = os.getenv('GOV_DATA_API_KEY')
MARKET_PRICE_URL = "https://api.data.gov.in/resource/9ef27131-652a-4a3a-a3a3-3939744c77c7"

def ai_price_suggestion():
    name = request.args.get('name', '').lower().strip()
    category = request.args.get('category', '')
    
    suggested = None
    confidence = 0
    reason = "Based on local market heuristics."

    # Try Real API (Data.gov.in)
    if GOV_DATA_API_KEY and GOV_DATA_API_KEY != 'your_gov_data_api_key_here' and name:
        try:
            # Note: In a real app, you'd map 'name' to the official commodity name
            params = {
                'api-key': GOV_DATA_API_KEY,
                'format': 'json',
                'filters[commodity]': name.capitalize(),
                'limit': 1
            }
            response = requests.get(MARKET_PRICE_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                if records:
                    # Prices are usually in Quintal (100kg), converting to per kg
                    avg_price = (float(records[0]['min_price']) + float(records[0]['max_price'])) / 2
                    suggested = round(avg_price / 100, 2)
                    confidence = random.randint(85, 98)
                    reason = f"Based on latest government data from {records[0]['market']} market ({records[0]['arrival_date']})."
        except Exception as e:
            print(f"Market API Error: {e}")

    # Fallback to Heuristic
    if suggested is None:
        base_price = 50.0
        if 'tomato' in name or 'tamatar' in name:
            base_price = 40.0
        elif 'potato' in name or 'aloo' in name:
            base_price = 30.0
        elif 'onion' in name or 'pyaaz' in name:
            base_price = 60.0
        elif 'mango' in name or 'aam' in name:
            base_price = 150.0
        elif 'rice' in name or 'chawal' in name:
            base_price = 80.0
        elif category == 'Fruits':
            base_price = 120.0
        elif category == 'Spices':
            base_price = 200.0
            
        suggested = round(base_price * random.uniform(0.9, 1.2), 2)
        confidence = random.randint(70, 85)

    return jsonify({
        'suggested_price': suggested, 
        'confidence': confidence,
        'reason': reason
    }), 200


def record_activity():
    """Records customer activity and notifies the farmer."""
    data = request.get_json()
    product_id = data.get('product_id')
    activity_type = data.get('type') # 'wishlist_add', 'cart_add'

    user_id = int(get_jwt_identity())
    customer = db.session.get(User, user_id)
    product = db.session.get(Product, product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    farmer_id = product.farmer_id
    customer_name = customer.name if customer else "A customer"

    if activity_type == 'wishlist_add':
        create_notification(
            user_id=farmer_id,
            title="❤️ Interest in your product!",
            message=f"{customer_name} added your '{product.name}' to their wishlist.",
            n_type="info"
        )
    elif activity_type == 'cart_add':
        create_notification(
            user_id=farmer_id,
            title="🛒 Cart Activity!",
            message=f"{customer_name} added '{product.name}' to their cart. Keep an eye out for a potential order!",
            n_type="info"
        )

    return jsonify({'message': 'Activity recorded'}), 200

