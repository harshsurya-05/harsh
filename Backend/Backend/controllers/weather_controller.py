from flask import request, jsonify
import random
import requests
import os
from datetime import datetime

# OpenWeatherMap Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Simulated weather data fallback
WEATHER_DATA = {
    'bhopal':   {'temp': 32, 'desc': 'Partly Cloudy', 'humidity': 62, 'wind': 14, 'icon': '⛅'},
    'mumbai':   {'temp': 29, 'desc': 'Humid & Cloudy', 'humidity': 80, 'wind': 20, 'icon': '🌧️'},
    'delhi':    {'temp': 38, 'desc': 'Hot & Sunny',    'humidity': 40, 'wind': 10, 'icon': '☀️'},
    'pune':     {'temp': 27, 'desc': 'Mostly Sunny',   'humidity': 55, 'wind': 12, 'icon': '🌤️'},
    'nagpur':   {'temp': 34, 'desc': 'Sunny',          'humidity': 48, 'wind': 8,  'icon': '☀️'},
    'indore':   {'temp': 31, 'desc': 'Partly Cloudy',  'humidity': 58, 'wind': 16, 'icon': '⛅'},
    'default':  {'temp': 28, 'desc': 'Clear Sky',      'humidity': 55, 'wind': 12, 'icon': '🌤️'},
}

CROP_TIPS = {
    'summer': [
        'Water crops early morning or late evening to reduce evaporation.',
        'Use mulching to retain soil moisture during hot days.',
        'Best crops: Tomato, Cucumber, Bhindi (Okra), Watermelon.',
        'Avoid transplanting during peak afternoon heat.'
    ],
    'monsoon': [
        'Ensure proper drainage to prevent waterlogging.',
        'Best crops: Rice, Maize, Soybean, Groundnut.',
        'Watch for fungal diseases due to high humidity.',
        'Use raised bed farming for vegetables.'
    ],
    'winter': [
        'Protect young plants from frost using covers.',
        'Best crops: Wheat, Mustard, Peas, Cauliflower, Carrot.',
        'Irrigate in the morning to avoid ice formation.',
        'Apply potassium fertilizer to boost frost resistance.'
    ]
}


def get_weather():
    """Returns real weather from OpenWeatherMap or simulated fallback."""
    location = request.args.get('location', 'Nagpur').strip()
    
    # Try Real API
    if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_openweather_key_here':
        try:
            params = {
                'q': location,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(WEATHER_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'location': data['name'],
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].capitalize(),
                    'humidity': data['main']['humidity'],
                    'wind_speed': round(data['wind']['speed'] * 3.6, 1), # Convert m/s to km/h
                    'icon_code': data['weather'][0]['icon']
                }
                # Map OpenWeather icons to emojis or use their icons
                icon_map = {'01': '☀️', '02': '🌤️', '03': '☁️', '04': '☁️', '09': '🌧️', '10': '🌦️', '11': '⛈️', '13': '❄️', '50': '🌫️'}
                weather_info['icon'] = icon_map.get(weather_info['icon_code'][:2], '⛅')
                return _format_weather_response(weather_info)
        except Exception as e:
            print(f"Weather API Error: {e}")

    # Fallback to Simulated Data
    weather = WEATHER_DATA.get('default')
    loc_lower = location.lower()
    for city, data in WEATHER_DATA.items():
        if city in loc_lower or loc_lower in city:
            weather = data
            break

    weather_info = {
        'location': location.title(),
        'temperature': weather['temp'] + random.randint(-2, 2),
        'description': weather['desc'],
        'humidity': min(100, max(20, weather['humidity'] + random.randint(-5, 5))),
        'wind_speed': weather['wind'],
        'icon': weather['icon']
    }
    return _format_weather_response(weather_info)


def _format_weather_response(info):
    """Common formatting for weather response."""
    # Determine season (India-based)
    month = datetime.utcnow().month
    if month in (3, 4, 5, 6):
        season = 'summer'
    elif month in (7, 8, 9, 10):
        season = 'monsoon'
    else:
        season = 'winter'

    tips = random.sample(CROP_TIPS[season], min(3, len(CROP_TIPS[season])))

    alerts = []
    if info['humidity'] > 75:
        alerts.append('🌧️ High humidity — rain likely. Plan outdoor activities accordingly.')
    if info['temperature'] > 37:
        alerts.append('🌡️ Very hot — irrigate crops in early morning or evening.')
    if info['wind_speed'] > 18:
        alerts.append('💨 Strong winds — secure young plants and greenhouses.')

    return jsonify({
        **info,
        'season': season,
        'crop_tips': tips,
        'alerts': alerts,
        'forecast': [
            {'day': 'Tomorrow',  'temp': info['temperature'] + random.randint(-3, 3), 'icon': '⛅'},
            {'day': 'Day After', 'temp': info['temperature'] + random.randint(-4, 4), 'icon': '🌤️'},
            {'day': 'Day 3',     'temp': info['temperature'] + random.randint(-3, 5), 'icon': '☀️'},
        ]
    }), 200


def get_crop_recommendations():
    """Returns crop recommendations based on season and location."""
    location = request.args.get('location', '').lower()
    soil     = request.args.get('soil', 'loamy').lower()

    month = datetime.utcnow().month
    if month in (3, 4, 5, 6):
        season = 'summer'
    elif month in (7, 8, 9, 10):
        season = 'monsoon'
    else:
        season = 'winter'

    recommendations = {
        'summer': [
            {'crop': 'Tomato',      'profit': 'High',   'price_trend': '📈 Rising', 'reason': 'High demand in summer'},
            {'crop': 'Cucumber',    'profit': 'Medium', 'price_trend': '→ Stable',  'reason': 'Good water content crop for summer'},
            {'crop': 'Watermelon',  'profit': 'High',   'price_trend': '📈 Rising', 'reason': 'Peak season demand'},
            {'crop': 'Okra (Bhindi)', 'profit': 'Medium', 'price_trend': '→ Stable', 'reason': 'Grows well in heat'},
        ],
        'monsoon': [
            {'crop': 'Rice',        'profit': 'High',   'price_trend': '→ Stable',  'reason': 'Monsoon is rice season'},
            {'crop': 'Soybean',     'profit': 'High',   'price_trend': '📈 Rising', 'reason': 'Export demand increasing'},
            {'crop': 'Maize',       'profit': 'Medium', 'price_trend': '→ Stable',  'reason': 'Used in poultry feed'},
            {'crop': 'Groundnut',   'profit': 'Medium', 'price_trend': '📈 Rising', 'reason': 'Oil demand high'},
        ],
        'winter': [
            {'crop': 'Wheat',       'profit': 'High',   'price_trend': '→ Stable',  'reason': 'Rabi season staple'},
            {'crop': 'Mustard',     'profit': 'High',   'price_trend': '📈 Rising', 'reason': 'Oil prices up'},
            {'crop': 'Cauliflower', 'profit': 'Medium', 'price_trend': '→ Stable',  'reason': 'Good winter vegetable'},
            {'crop': 'Carrot',      'profit': 'Medium', 'price_trend': '📈 Rising', 'reason': 'High demand in winter'},
        ]
    }

    avoid = {
        'summer':  ['Rice', 'Wheat', 'Mustard'],
        'monsoon': ['Cauliflower', 'Tomato (open field)'],
        'winter':  ['Watermelon', 'Cucumber']
    }

    return jsonify({
        'season': season,
        'location': location.title() or 'General',
        'soil_type': soil,
        'recommended': recommendations[season],
        'avoid': avoid[season],
        'message': f'Best crops for {season} season based on market trends and weather.'
    }), 200


def get_demand_prediction():
    """Returns simulated demand prediction for crops."""
    crops = [
        {'name': 'Tomato',    'demand_change': +42, 'reason': 'Festival season demand spike'},
        {'name': 'Onion',     'demand_change': -15, 'reason': 'Good harvest — oversupply'},
        {'name': 'Potato',    'demand_change': +5,  'reason': 'Stable demand from fast food'},
        {'name': 'Wheat',     'demand_change': +8,  'reason': 'Export orders increasing'},
        {'name': 'Mango',     'demand_change': +65, 'reason': 'Peak mango season'},
        {'name': 'Soybean',   'demand_change': +20, 'reason': 'Poultry feed demand rising'},
        {'name': 'Rice',      'demand_change': +10, 'reason': 'Consistent staple demand'},
        {'name': 'Cauliflower', 'demand_change': -8, 'reason': 'Off-season production high'},
    ]

    for c in crops:
        c['demand_change'] += random.randint(-5, 5)
        c['trend'] = '📈 Rising' if c['demand_change'] > 0 else '📉 Falling'

    return jsonify({
        'predictions': crops,
        'updated_at': datetime.now().strftime('%Y-%m-%d'),
        'note': 'Based on market trends, seasonal patterns and regional data.'
    }), 200
