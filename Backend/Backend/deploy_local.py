import os
import sys
from waitress import serve
from app import app

def start_production_server():
    print("=========================================")
    print("   AgroHub Production Server (Waitress)  ")
    print("=========================================")
    print("Starting server on http://0.0.0.0:5000")
    print("Press Ctrl+C to stop.")
    
    # In production, we usually want to set FLASK_ENV to production
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = '0'
    
    try:
        serve(app, host='0.0.0.0', port=5000, threads=6)
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)

if __name__ == "__main__":
    start_production_server()
