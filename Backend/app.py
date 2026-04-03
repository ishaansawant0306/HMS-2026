from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from models import db
from routes import register_blueprints
from init_db import init_admin


def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app, origins=['http://localhost:3000', 'http://localhost:8080', 'http://127.0.0.1:3000'])
    
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms2026.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this-in-production'  # Change in production!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    register_blueprints(app)
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Initialize admin user
        init_admin()
    
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)




