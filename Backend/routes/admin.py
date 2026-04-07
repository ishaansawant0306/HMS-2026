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
    try:
        total_doctors = db.session.query(Doctor).filter(Doctor.is_blacklisted == False).count()
        total_patients = db.session.query(Patient).filter(Patient.is_blacklisted == False).count()
        total_appointments = Appointment.query.count()
        
        # Status breakdown
        upcoming = Appointment.query.filter(Appointment.status == 'Booked').count()
        completed = Appointment.query.filter(Appointment.status == 'Completed').count()
        cancelled = Appointment.query.filter(Appointment.status == 'Cancelled').count()
        
        return jsonify({
            'status': 'success',
            'dashboard': {
                'total_doctors': total_doctors,
                'total_patients': total_patients,
                'total_appointments': total_appointments,
                'upcoming_appointments': upcoming,
                'completed_appointments': completed,
                'cancelled_appointments': cancelled
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_all_doctors():
    """
    Get list of all doctors. By default returns non-blacklisted doctors.
    Query parameter: include_blacklisted (true to include blacklisted doctors)
    Query parameter: search (to search by name or specialization)
    """
    try:
        include_blacklisted = request.args.get('include_blacklisted', 'false').lower() == 'true'
        search_query = request.args.get('search', '').strip()
        
        query = Doctor.query.join(User)
        
        if not include_blacklisted:
            query = query.filter(Doctor.is_blacklisted == False)
        
        if search_query:
            query = query.filter(
                (User.username.ilike(f'%{search_query}%')) | 
                (Doctor.specialization.ilike(f'%{search_query}%'))
            )
        
        doctors = query.all()
        doctor_list = []
        
        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'name': doctor.user.username,
                'email': doctor.user.email,
                'specialization': doctor.specialization,
                'availability': doctor.availability,
                'is_blacklisted': doctor.is_blacklisted,
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
        # Disable doctor's user account to prevent login
        doctor.user.is_active = False
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor blacklisted successfully',
            'doctor': {
                'id': doctor.id,
                'name': doctor.user.username,
                'is_blacklisted': doctor.is_blacklisted
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors/<int:doctor_id>/unblacklist', methods=['POST'])
@jwt_required()
@require_role('admin')
def unblacklist_doctor(doctor_id):
    """
    Unblacklist a doctor to restore access
    """
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        doctor.is_blacklisted = False
        # Re-enable doctor's user account
        doctor.user.is_active = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor unblacklisted successfully',
            'doctor': {
                'id': doctor.id,
                'name': doctor.user.username,
                'is_blacklisted': doctor.is_blacklisted
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
@require_role('admin')
def delete_doctor(doctor_id):
    """
    Permanently delete a doctor from the system
    """
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        # Delete associated appointments first
        Appointment.query.filter_by(doctor_id=doctor_id).delete()
        
        # Delete the doctor and associated user
        db.session.delete(doctor)
        db.session.delete(doctor.user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctor deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_all_patients():
    """
    Get list of all patients. By default returns non-blacklisted patients.
    Query parameter: include_blacklisted (true to include blacklisted patients)
    Query parameter: search (to search by name or email)
    """
    try:
        include_blacklisted = request.args.get('include_blacklisted', 'false').lower() == 'true'
        search_query = request.args.get('search', '').strip()
        
        query = Patient.query.join(User)
        
        if not include_blacklisted:
            query = query.filter(Patient.is_blacklisted == False)
        
        if search_query:
            query = query.filter(
                (User.username.ilike(f'%{search_query}%')) | 
                (User.email.ilike(f'%{search_query}%'))
            )
        
        patients = query.all()
        
        patient_list = []
        for patient in patients:
            patient_data = {
                'id': patient.id,
                'name': patient.user.username,
                'username': patient.user.username,
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender,
                'contact_number': patient.contact_number,
                'address': patient.address,
                'height': patient.height,
                'weight': patient.weight,
                'is_blacklisted': patient.is_blacklisted,
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
        # Disable patient's user account to prevent login
        patient.user.is_active = False
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Patient blacklisted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/patients/<int:patient_id>/unblacklist', methods=['POST'])
@jwt_required()
@require_role('admin')
def unblacklist_patient(patient_id):
    """
    Unblacklist a patient to restore access
    """
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        patient.is_blacklisted = False
        # Re-enable patient's user account
        patient.user.is_active = True
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Patient unblacklisted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/appointments/past', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_past_appointments():
    """
    Get all completed and cancelled appointments
    """
    try:
        appointments = Appointment.query.filter(
            Appointment.status.in_(['Completed', 'Cancelled'])
        ).all()
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


@admin_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
@require_role('admin')
def update_patient(patient_id):
    """
    Update patient information
    """
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        data = request.get_json()
        
        # Update user fields if provided
        if 'username' in data:
            patient.user.username = data['username']
        if 'email' in data:
            # Check if email already in use
            if User.query.filter(User.email == data['email'], User.id != patient.user_id).first():
                return jsonify({'error': 'Email already in use'}), 400
            patient.user.email = data['email']
        
        # Update patient fields if provided
        if 'age' in data:
            patient.age = data['age']
        if 'gender' in data:
            patient.gender = data['gender']
        if 'contact_number' in data:
            patient.contact_number = data['contact_number']
        if 'address' in data:
            patient.address = data['address']
        if 'height' in data:
            patient.height = data['height']
        if 'weight' in data:
            patient.weight = data['weight']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Patient updated successfully',
            'patient': {
                'id': patient.id,
                'name': patient.user.username,
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender,
                'contact_number': patient.contact_number,
                'address': patient.address
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
