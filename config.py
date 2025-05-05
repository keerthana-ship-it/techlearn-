import os
from urllib.parse import urlparse

class Config:
    """Base configuration class."""
    DEBUG = True
    SECRET_KEY = os.environ.get("SESSION_SECRET", "dev_key_replace_in_production")
    
    # Database configuration
    if os.environ.get("DATABASE_URL"):
        # Handle Heroku/Render PostgreSQL URL
        url = urlparse(os.environ.get("DATABASE_URL"))
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{url.username}:{url.password}@{url.hostname}:{url.port}{url.path}"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///techlearn.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Mail configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "learnconnectcrux@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "learnconnectcrux@gmail.com")
    
    # Support contact info
    SUPPORT_EMAIL = "learnconnectcrux@gmail.com"
    SUPPORT_PHONE = "+91 9444041192"
    
    # Default settings
    DEFAULT_LOCATION = "Chennai"
