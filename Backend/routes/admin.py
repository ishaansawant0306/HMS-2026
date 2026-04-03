"""
Admin routes for Hospital Management System
Handle admin-specific operations like managing doctors, viewing appointments, etc.
"""
from flask import Blueprint, request, jsonify
from models import db, User, Doctor, Patient, Appointment, Department
from utils.auth import require_role, hash_password
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('admin')
def dashboard():
    """
    Admin dashboard endpoint - displays key statistics
    Returns: Total doctors, patients, and appointments count
    """
    try:
        total_doctors = Doctor.query.count()
        total_patients = Patient.query.count()
        total_appointments = Appointment.query.count()
        upcoming_appointments = Appointment.query.filter(
            Appointment.status == 'Booked'
        ).count()
        
        return jsonify({
            'status': 'success',
            'dashboard': {
                'total_doctors': total_doctors,
                'total_patients': total_patients,
                'total_appointments': total_appointments,
                'upcoming_appointments': upcoming_appointments
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_all_doctors():
    """
    Get list of all doctors
    """
    try:
        doctors = Doctor.query.filter(Doctor.is_blacklisted == False).all()
        doctor_list = []
        
        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'name': doctor.user.username,
                'email': doctor.user.email,
                'specialization': doctor.specialization,
                'availability': doctor.availability,
                'created_at': doctor.created_at.isoformat()
            }
            doctor_list.append(doctor_data)
        
        return jsonify({
            'status': 'success',
            'doctors': doctor_list,
            'count': len(doctor_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors', methods=['POST'])
@jwt_required()
@require_role('admin')
def add_doctor():
    """
    Add a new doctor to the system
    Required fields: username, email, password, specialization
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'specialization']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            role='doctor',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create doctor profile
        doctor = Doctor(
            user_id=user.id,
            specialization=data['specialization'],
            availability=data.get('availability', '{}'),
            is_blacklisted=False
        )
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor added successfully',
            'doctor': {
                'id': doctor.id,
                'name': user.username,
                'email': user.email,
                'specialization': doctor.specialization
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@jwt_required()
@require_role('admin')
def update_doctor(doctor_id):
    """
    Update doctor information
    """
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        data = request.get_json()
        
        # Update user fields if provided
        if 'username' in data:
            doctor.user.username = data['username']
        if 'email' in data:
            doctor.user.email = data['email']
        
        # Update doctor fields if provided
        if 'specialization' in data:
            doctor.specialization = data['specialization']
        if 'availability' in data:
            doctor.availability = data['availability']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor updated successfully',
            'doctor': {
                'id': doctor.id,
                'name': doctor.user.username,
                'email': doctor.user.email,
                'specialization': doctor.specialization
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors/<int:doctor_id>/blacklist', methods=['POST'])
@jwt_required()
@require_role('admin')
def blacklist_doctor(doctor_id):
    """
    Blacklist a doctor (soft delete)
    """
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        doctor.is_blacklisted = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor blacklisted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/appointments', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_all_appointments():
    """
    Get all appointments (upcoming and past)
    """
    try:
        appointments = Appointment.query.all()
        appointment_list = []
        
        for appointment in appointments:
            appointment_data = {
                'id': appointment.id,
                'doctor_name': appointment.doctor.user.username,
                'patient_name': appointment.patient.user.username,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status,
                'created_at': appointment.created_at.isoformat()
            }
            appointment_list.append(appointment_data)
        
        return jsonify({
            'status': 'success',
            'appointments': appointment_list,
            'count': len(appointment_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/search/patients', methods=['GET'])
@jwt_required()
@require_role('admin')
def search_patients():
    """
    Search for patients by name or email
    Query parameter: q (search query)
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        patients = Patient.query.join(User).filter(
            (User.username.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%')),
            Patient.is_blacklisted == False
        ).all()
        
        patient_list = []
        for patient in patients:
            patient_data = {
                'id': patient.id,
                'name': patient.user.username,
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender,
                'contact_number': patient.contact_number,
                'created_at': patient.created_at.isoformat()
            }
            patient_list.append(patient_data)
        
        return jsonify({
            'status': 'success',
            'patients': patient_list,
            'count': len(patient_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/search/doctors', methods=['GET'])
@jwt_required()
@require_role('admin')
def search_doctors():
    """
    Search for doctors by name or specialization
    Query parameter: q (search query)
    """
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        doctors = Doctor.query.join(User).filter(
            (User.username.ilike(f'%{query}%')) | (Doctor.specialization.ilike(f'%{query}%')),
            Doctor.is_blacklisted == False
        ).all()
        
        doctor_list = []
        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'name': doctor.user.username,
                'email': doctor.user.email,
                'specialization': doctor.specialization,
                'availability': doctor.availability,
                'created_at': doctor.created_at.isoformat()
            }
            doctor_list.append(doctor_data)
        
        return jsonify({
            'status': 'success',
            'doctors': doctor_list,
            'count': len(doctor_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/patients/<int:patient_id>/blacklist', methods=['POST'])
@jwt_required()
@require_role('admin')
def blacklist_patient(patient_id):
    """
    Blacklist a patient (soft delete)
    """
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        patient.is_blacklisted = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Patient blacklisted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
