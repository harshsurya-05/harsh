"""
Payment Service — Stub implementation.
Replace with real Razorpay/Stripe SDK calls by adding API keys to .env.
"""
import uuid
from app import db
from models.order_model import Payment


def process_payment(order_id: int, amount: float, method: str = 'card') -> dict:
    """
    Stub payment processor. Always returns success.
    In production, integrate Razorpay or Stripe here.
    """
    transaction_id = f'TXN_{uuid.uuid4().hex[:12].upper()}'

    payment = Payment(
        order_id=order_id,
        amount=amount,
        method=method,
        status='success',
        transaction_id=transaction_id
    )
    db.session.add(payment)
    # Don't commit here — caller commits

    return {
        'success': True,
        'transaction_id': transaction_id,
        'amount': amount,
        'method': method,
        'gateway': 'AgroHub Pay (Stub)',
        'message': 'Payment processed successfully'
    }


def refund_payment(transaction_id: str, amount: float) -> dict:
    """Stub refund processor."""
    return {
        'success': True,
        'refund_id': f'REF_{uuid.uuid4().hex[:10].upper()}',
        'amount': amount,
        'message': 'Refund initiated (stub)'
    }
