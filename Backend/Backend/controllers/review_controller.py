from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db
from models.review_model import Review
from models.product_model import Product


def submit_review():
    """Customer submits a review for a product."""
    customer_id = int(get_jwt_identity())
    data = request.get_json()

    product_id = data.get('product_id')
    rating     = float(data.get('rating', 0))
    review_txt = data.get('review', '').strip()

    if not product_id:
        return jsonify({'error': 'product_id is required'}), 400
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Check for duplicate review
    existing = Review.query.filter_by(product_id=product_id, customer_id=customer_id).first()
    if existing:
        existing.rating = rating
        existing.review = review_txt
        db.session.commit()
        return jsonify({'message': 'Review updated', 'review': existing.to_dict()}), 200

    review = Review(
        product_id=product_id,
        customer_id=customer_id,
        rating=rating,
        review=review_txt
    )
    db.session.add(review)

    # Update product rating average
    all_reviews = Review.query.filter_by(product_id=product_id).all()
    total_ratings = sum(r.rating for r in all_reviews) + rating
    product.rating = round(total_ratings / (len(all_reviews) + 1), 2)

    db.session.commit()
    return jsonify({'message': 'Review submitted', 'review': review.to_dict()}), 201


def get_product_reviews(product_id):
    """Get all reviews for a product."""
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return jsonify({'reviews': [r.to_dict() for r in reviews]}), 200


def get_my_reviews():
    """Get all reviews written by the logged-in customer."""
    customer_id = int(get_jwt_identity())
    reviews = Review.query.filter_by(customer_id=customer_id).order_by(Review.created_at.desc()).all()
    return jsonify({'reviews': [r.to_dict() for r in reviews]}), 200
