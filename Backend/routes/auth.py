"""
Authentication routes for Hospital Management System
Handle login/register for all user roles
"""
from flask import Blueprint, request, jsonify
from models import db, User, Patient, Doctor, Appointment  
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.auth import hash_password, verify_password
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register/patient', methods=['POST'])
def register_patient():
    """
    Patient registration endpoint
    Required fields: username, email, password, age, gender, contact_number
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'age', 'gender', 'contact_number']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'status': 'error', 'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'status': 'error', 'message': 'Email already exists'}), 400
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            role='patient',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create patient profile
        patient = Patient(
            user_id=user.id,
            contact_number=data['contact_number'],
            address=data.get('address', ''),
            age=data['age'],
            gender=data['gender'],
            height=data.get('height', 0.0),
            weight=data.get('weight', 0.0),
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


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint for all user roles (admin, doctor, patient)
    Returns JWT token and user info with dashboard redirect
    """
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
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