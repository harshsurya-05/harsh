from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app import db

# In a real app, we would have a Message model. 
# For now, we'll simulate a support response.

def send_support_message():
    data = request.get_json()
    message = data.get('message', '')
    user_id = get_jwt_identity()

    # Simulate AI Response
    responses = [
        "Hello! How can I help you with your AgroHub experience today?",
        "Our team will get back to you shortly regarding your query.",
        "To track your order, please visit the 'Delivery' section in your dashboard.",
        "Farmers can add products using the 'Product Management' tab."
    ]
    import random
    ai_reply = random.choice(responses)

    return jsonify({
        'status': 'sent',
        'reply': ai_reply
    }), 200
