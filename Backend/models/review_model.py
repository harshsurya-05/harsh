from extensions import db
from datetime import datetime


class Review(db.Model):
    __tablename__ = 'reviews'

    id          = db.Column(db.Integer, primary_key=True)
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating      = db.Column(db.Float, nullable=False)   # 1-5
    review      = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    customer    = db.relationship('User',    foreign_keys=[customer_id], lazy=True)
    product     = db.relationship('Product', foreign_keys=[product_id],  lazy=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'product_id':   self.product_id,
            'product_name': self.product.name if self.product else None,
            'customer_id':  self.customer_id,
            'customer_name':self.customer.name if self.customer else 'Customer',
            'rating':       self.rating,
            'review':       self.review,
            'created_at':   self.created_at.isoformat()
        }
