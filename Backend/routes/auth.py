
from flask import Blueprint, request, jsonify
from models import db, User, Patient, Doctor, Appointment
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.auth import hash_password, verify_password
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register/patient', methods=['POST'])
def register_patient():
    
     

      
    try:
        data = request.get_json() or {}

        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        age = data.get('age')
        location = data.get('location', '').strip()

        if not email or not password or not age or not location:
            return jsonify({'status': 'error', 'message': 'Email, password, age, and location are required.'}), 400

        username = data.get('username')
        if not username:
            username = email

        existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if existing_user:
            if existing_user.email == email:
                return jsonify({'status': 'error', 'message': 'Email already exists.'}), 400
            if existing_user.username == username:
                return jsonify({'status': 'error', 'message': 'Username already exists.'}), 400
            return jsonify({'status': 'error', 'message': 'A user with this email or username already exists.'}), 400

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role='patient',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()  # Get user ID without committing

        # Create patient profile
        patient = Patient(
            user_id=user.id,
            contact_number=data.get('contact_number', ''),
            address=location,
            age=int(age),
            gender=data.get('gender', 'unspecified'),
            height=float(data.get('height', 0.0) or 0.0),
            weight=float(data.get('weight', 0.0) or 0.0),
            is_blacklisted=False
        )
        db.session.add(patient)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Patient registered successfully',
            'patient': {
                'id': patient.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@auth_bp.route('/register', methods=['POST'])
def register_patient_alias():
    return register_patient()


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint for all user roles (admin, doctor, patient)
    Returns JWT token and user info with dashboard redirect
    """
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Email or username and password are required'}), 400

        identifier = data['email'].strip()
        user = User.query.filter(or_(User.email == identifier, User.username == identifier)).first()

        if not user or not verify_password(user.password_hash, data['password']):
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'status': 'error', 'message': 'User account is inactive'}), 403
        
        # Create JWT token
        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'role': user.role,
                'username': user.username
            }
        )
        
        # Determine redirect dashboard based on role
        dashboard_redirect = {
            'admin': '/api/admin/dashboard',
            'doctor': '/api/doctor/dashboard',
            'patient': '/api/patient/dashboard'
        }
        
        return jsonify({
            'status': 'success',
            'access_token': token,
            'token_type': 'Bearer',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            },
            'redirect': dashboard_redirect.get(user.role, '/dashboard')
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        return jsonify({
            'status': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500