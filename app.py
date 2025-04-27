import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Setup SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle proxy headers for proper URL generation
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.collect import collect_bp
    from routes.connect import connect_bp
    from routes.crux import crux_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(collect_bp, url_prefix='/collect')
    app.register_blueprint(connect_bp, url_prefix='/connect')
    app.register_blueprint(crux_bp, url_prefix='/crux')
    
    # Initialize database
    with app.app_context():
        # Import models to ensure they're registered with SQLAlchemy
        import models  # noqa: F401
        
        # Create database tables
        db.create_all()
    
    return app

# Create the app instance
app = create_app()

# Import user loader
from models import User

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))
