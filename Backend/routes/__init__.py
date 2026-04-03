from .auth import auth_bp
from .admin import admin_bp
from .doctor import doctor_bp
from .patient import patient_bp

def register_blueprints(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    