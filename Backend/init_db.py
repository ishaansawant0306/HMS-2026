
from models import db, User, Doctor
from utils.auth import hash_password

# initialises  admin user
def init_admin():
    existing_admin = User.query.filter_by(role='admin').first()
    
    if existing_admin:
        print(" Admin user already exists")
    else:
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
            print(" Admin user created successfully")
            print(f"  Username: admin")
            print(f"  Email: admin@hospital.com")
            print(f"  Password: admin123")
            print("    Please change the password after first login!")
        except Exception as e:
            db.session.rollback()
            print(f" Error creating admin user: {str(e)}")
            raise


def remove_test_doctor():
    test_user = User.query.filter_by(email='testdoctor@hospital.com', role='doctor').first()
    if not test_user:
        print(" Legacy test doctor not present")
        return

    try:
        doctor = Doctor.query.filter_by(user_id=test_user.id).first()
        if doctor:
            db.session.delete(doctor)
        db.session.delete(test_user)
        db.session.commit()
        print(" Legacy test doctor removed")
    except Exception as e:
        db.session.rollback()
        print(f" Error removing legacy test doctor: {str(e)}")
        raise
