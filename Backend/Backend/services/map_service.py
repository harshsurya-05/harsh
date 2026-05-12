"""
Map Service — Simulates GPS coordinates for delivery tracking.
Uses a random walk from an initial position around India.
"""
import random


# Default center: New Delhi, India
DEFAULT_LAT = 28.6139
DEFAULT_LNG = 77.2090

# Step size for simulated movement (~100-500 meters per update)
STEP = 0.004


def get_initial_coordinates(lat: float = None, lng: float = None):
    """Return starting coordinates for a delivery."""
    base_lat = lat or DEFAULT_LAT
    base_lng = lng or DEFAULT_LNG
    # Add small random offset to simulate different farm locations
    return (
        round(base_lat + random.uniform(-0.5, 0.5), 6),
        round(base_lng + random.uniform(-0.5, 0.5), 6)
    )


def simulate_movement(current_lat: float, current_lng: float):
    """
    Simulates the delivery moving slightly toward the customer.
    In production, replace with real GPS data from the delivery app.
    """
    if current_lat is None or current_lng is None:
        return get_initial_coordinates()

    delta_lat = random.uniform(-STEP, STEP)
    delta_lng = random.uniform(-STEP, STEP)

    new_lat = round(current_lat + delta_lat, 6)
    new_lng = round(current_lng + delta_lng, 6)

    return new_lat, new_lng


def geocode_address(address: str) -> tuple:
    """
    Stub geocoder — returns approximate Delhi coordinates.
    Replace with Google Maps Geocoding API or Nominatim in production.
    """
    return get_initial_coordinates()
