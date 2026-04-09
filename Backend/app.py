from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load .env variables FIRST before anything else
load_dotenv()

from extensions import db, cache, mail
from routes import register_blueprints
from init_db import init_admin, remove_test_doctor


def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app, origins=[
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:3001',
        'http://127.0.0.1:3001',
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:8080'
    ])
    
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms2026.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Celery Configuration
    app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Email Configuration (Optional - for sending reminders and reports)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'localhost')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', True)
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@medizentrum.com')

    # Caching Configuration
    app.config['CACHE_TYPE'] = os.getenv('CACHE_TYPE', 'RedisCache')
    app.config['CACHE_REDIS_URL'] = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '60'))
    app.config['CACHE_KEY_PREFIX'] = os.getenv('CACHE_KEY_PREFIX', 'hms_')
    
    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize Celery
    try:
        from celery_config import make_celery
        celery = make_celery(app)
        app.celery = celery
    except Exception as e:
        print(f"Warning: Celery not initialized: {str(e)}")
    
    register_blueprints(app)
    import tasks  # Ensure Celery tasks are discovered when the app starts
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Initialize admin user and clean up legacy seed data
        init_admin()
        remove_test_doctor()
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




