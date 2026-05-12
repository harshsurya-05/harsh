"""
AI Service — Product recommendation and seasonal suggestions.
Stub implementation ready for LLM/ML integration.
"""
from datetime import datetime


SEASONAL_RECOMMENDATIONS = {
    'summer': {
        'categories': ['Fruits', 'Vegetables'],
        'products': ['Mangoes', 'Watermelon', 'Cucumber', 'Tomatoes', 'Bitter Gourd'],
        'tip': 'Stay hydrated! Summer fruits are rich in water content.'
    },
    'monsoon': {
        'categories': ['Vegetables', 'Grains'],
        'products': ['Corn', 'Green Chilli', 'Ginger', 'Turmeric', 'Rice'],
        'tip': 'Monsoon is ideal for root vegetables and grains.'
    },
    'winter': {
        'categories': ['Vegetables', 'Spices'],
        'products': ['Spinach', 'Cauliflower', 'Peas', 'Mustard Greens', 'Carrots'],
        'tip': 'Winter greens are packed with vitamins and minerals.'
    },
    'spring': {
        'categories': ['Fruits', 'Pulses'],
        'products': ['Strawberries', 'Lychee', 'Moong Dal', 'Chana Dal', 'Raw Mango'],
        'tip': 'Spring harvest brings the freshest legumes and early fruits.'
    }
}


def get_season() -> str:
    month = datetime.utcnow().month
    if month in (3, 4, 5):
        return 'spring'
    elif month in (6, 7, 8, 9):
        return 'monsoon'
    elif month in (10, 11):
        return 'winter'
    else:
        return 'summer'


def get_recommendations(category: str = None, user_history: list = None) -> dict:
    """
    Returns seasonal product recommendations.
    In production: replace with ML model or LLM (e.g., Gemini API).
    """
    season = get_season()
    data = SEASONAL_RECOMMENDATIONS[season]

    return {
        'season': season,
        'recommended_categories': data['categories'],
        'recommended_products': data['products'],
        'seasonal_tip': data['tip'],
        'source': 'AgroHub AI (Seasonal Engine v1.0)'
    }


def predict_price_trend(product_name: str) -> dict:
    """
    Stub price trend predictor.
    In production: use time-series ML model.
    """
    import random
    trend = random.choice(['rising', 'stable', 'falling'])
    change = round(random.uniform(2, 15), 1)
    return {
        'product': product_name,
        'trend': trend,
        'expected_change_pct': change if trend != 'falling' else -change,
        'confidence': round(random.uniform(0.6, 0.95), 2),
        'source': 'AgroHub Price AI (Stub)'
    }
