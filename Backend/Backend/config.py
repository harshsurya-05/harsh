import os
import cloudinary
from dotenv import load_dotenv

# Use absolute path so it works regardless of working directory
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

# Cloudinary Configuration
cloudinary.config(
  cloudinary_url = os.environ.get('CLOUDINARY_URL')
)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agrohub-default-secret')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'agrohub-jwt-default')

    # Fix deprecated postgres:// prefix for SQLAlchemy 2.x
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///agrohub.db')
    
    if _db_url.startswith('sqlite:///'):
        _db_filename = _db_url.replace('sqlite:///', '')
        _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), _db_filename)
        _db_url = f"sqlite:///{_db_path}"

    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
    }
    
    # JWT Config
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)) # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400 * 30 # 30 days
    
    # Mail Config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    # CORS
    CORS_ORIGINS = ["*"]
