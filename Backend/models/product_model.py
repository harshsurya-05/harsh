from extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id          = db.Column(db.Integer, primary_key=True)
    farmer_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name        = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, nullable=False, default=0)
    unit        = db.Column(db.String(30), nullable=False, default='kg')
    image_url   = db.Column(db.String(500), nullable=True)
    is_active   = db.Column(db.Boolean, default=True)
    rating      = db.Column(db.Float, default=0.0)
    rating_count= db.Column(db.Integer, default=0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship — overlaps declared to silence SQLAlchemy warning
    reviews     = db.relationship('Review', lazy=True,
                                  foreign_keys='Review.product_id',
                                  overlaps='product')

    def to_dict(self):
        return {
            'id':           self.id,
            'farmer_id':    self.farmer_id,
            'farmer_name':  self.farmer.name if self.farmer else None,
            'name':         self.name,
            'category':     self.category,
            'description':  self.description,
            'price':        self.price,
            'stock':        self.stock,
            'unit':         self.unit,
            'image_url':    self.image_url,
            'is_active':    self.is_active,
            'rating':       round(self.rating, 1) if self.rating else 0.0,
            'rating_count': self.rating_count,
            'created_at':   self.created_at.isoformat()
        }
