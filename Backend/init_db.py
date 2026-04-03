"""
Admin initialization script - creates a default admin user if it doesn't exist.
This should be run when the application starts.
"""
from models import db, User
from utils.auth import hash_password


def init_admin():
    """
    Initialize admin user if it doesn't already exist in the database.
    
    Default admin credentials:
        username: admin
        email: admin@hospital.com
        password: admin123 (should be changed in production)
    """
    # Check if admin already exists
    existing_admin = User.query.filter_by(role='admin').first()
    
    if existing_admin:
        print("✓ Admin user already exists")
        return
    
    # Create default admin user
    admin_user = User(
        username='admin',
        email='admin@hospital.com',
        password_hash=hash_password('admin123'),
        role='admin',
        is_active=True
    )
    
    try:
        db.session.add(admin_user)
        db.session.commit()
        print("✓ Admin user created successfully")
        print(f"  Username: admin")
        print(f"  Email: admin@hospital.com")
        print(f"  Password: admin123")
        print("  ⚠️  Please change the password after first login!")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error creating admin user: {str(e)}")
        raise
