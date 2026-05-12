from flask import Blueprint
from controllers.weather_controller import get_weather, get_crop_recommendations, get_demand_prediction

weather_bp = Blueprint('weather', __name__)

weather_bp.route('/', methods=['GET'])(get_weather)
weather_bp.route('/crops', methods=['GET'])(get_crop_recommendations)
weather_bp.route('/demand', methods=['GET'])(get_demand_prediction)
