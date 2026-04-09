from app import app, db
from models import User
from utils.auth import hash_password

with app.app_context():
    
    admin = User.query.filter_by(email='admin@hospital.com').first()
    if admin:
        db.session.delete(admin)
        db.session.commit()
    
    # admin
    admin = User(
        username='admin',
        email='admin@hospital.com',
        password_hash=hash_password('admin123'),
        role='admin',
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print("  Admin created: email=admin@hospital.com, password=admin123")