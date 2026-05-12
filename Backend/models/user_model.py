from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')  # 'farmer' | 'customer' | 'delivery'
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    profile_photo = db.Column(db.String(500), nullable=True)

    # --- Common fields ---
    preferred_language = db.Column(db.String(20), default='english')  # english | hindi | marathi | etc.
    referral_code = db.Column(db.String(20), unique=True, nullable=True)
    referred_by = db.Column(db.String(20), nullable=True)   # referral code of whoever referred this user
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    gps_lat = db.Column(db.Float, nullable=True)
    gps_lng = db.Column(db.Float, nullable=True)
    notification_prefs = db.Column(db.String(200), default='email,sms')  # comma-separated

    # --- Farmer-specific ---
    farm_location = db.Column(db.String(200), nullable=True)   # Village / Area name
    farming_type = db.Column(db.String(50), nullable=True)     # Organic / Regular / Mixed
    crops_category = db.Column(db.String(200), nullable=True)  # Comma-separated: Fruits,Vegetables
    quantity_available = db.Column(db.String(100), nullable=True)  # e.g. "500 kg wheat"
    upi_id = db.Column(db.String(100), nullable=True)          # UPI ID for payouts
    bank_account = db.Column(db.String(50), nullable=True)     # Optional bank account

    # --- Customer-specific ---
    delivery_addresses = db.Column(db.Text, nullable=True)     # JSON string: list of addresses
    payment_method = db.Column(db.String(30), default='cod')   # upi | card | cod

    # --- Delivery Boy specific ---
    vehicle_type = db.Column(db.String(50), nullable=True)     # Bike / Cycle / Auto / Car
    license_number = db.Column(db.String(50), nullable=True)
    availability_status = db.Column(db.String(20), default='offline')  # online | offline
    
    # Auth Security
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', backref='farmer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'address': self.address,
            'profile_photo': self.profile_photo,
            'preferred_language': self.preferred_language,
            'referral_code': self.referral_code,
            'referred_by': self.referred_by,
            'rating': round(self.rating, 1) if self.rating else 0.0,
            'rating_count': self.rating_count,
            'gps_lat': self.gps_lat,
            'gps_lng': self.gps_lng,
            'notification_prefs': self.notification_prefs,
            # Farmer
            'farm_location': self.farm_location,
            'farming_type': self.farming_type,
            'crops_category': self.crops_category,
            'quantity_available': self.quantity_available,
            'upi_id': self.upi_id,
            'bank_account': self.bank_account,
            # Customer
            'delivery_addresses': self.delivery_addresses,
            'payment_method': self.payment_method,
            # Delivery
            'vehicle_type': self.vehicle_type,
            'license_number': self.license_number,
            'availability_status': self.availability_status,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
