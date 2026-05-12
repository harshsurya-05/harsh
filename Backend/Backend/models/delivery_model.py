from extensions import db
from datetime import datetime


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    delivery_address = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='preparing')
    # preparing | picked_up | in_transit | out_for_delivery | delivered
    courier_name = db.Column(db.String(100), nullable=True)
    tracking_number = db.Column(db.String(100), nullable=True)
    current_lat = db.Column(db.Float, nullable=True)
    current_lng = db.Column(db.Float, nullable=True)
    estimated_delivery = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'delivery_address': self.delivery_address,
            'status': self.status,
            'courier_name': self.courier_name,
            'tracking_number': self.tracking_number,
            'current_lat': self.current_lat,
            'current_lng': self.current_lng,
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'updated_at': self.updated_at.isoformat()
        }
