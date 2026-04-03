
from flask import Blueprint, request, jsonify
from models import db, User, Doctor, Patient, Appointment, Treatment, Department
from utils.auth import require_role
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import json

patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')


@patient_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('patient')
def dashboard():
    """
    Patient dashboard - shows appointment status, available specializations, etc.
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        # Get upcoming appointments
        today = datetime.now().date()
        upcoming_appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.date >= today,
            Appointment.status.in_(['Booked', 'Completed'])
        ).all()
        
        # Get all specializations
        specializations = db.session.query(Doctor.specialization).distinct().all()
        specializations_list = [s[0] for s in specializations if s[0]]
        
        appointments_list = []
        for appointment in upcoming_appointments:
            appointment_data = {
                'id': appointment.id,
                'doctor_name': appointment.doctor.user.username,
                'specialization': appointment.doctor.specialization,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status
            }
            appointments_list.append(appointment_data)
        
        return jsonify({
            'status': 'success',
            'patient': {
                'id': patient.id,
                'name': patient.user.username,
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender
            },
            'upcoming_appointments': appointments_list,
            'upcoming_count': len(appointments_list),
            'specializations': specializations_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_profile():
    """
    Get patient's profile information
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        return jsonify({
            'status': 'success',
            'patient': {
                'id': patient.id,
                'username': patient.user.username,
                'email': patient.user.email,
                'contact_number': patient.contact_number,
                'address': patient.address,
                'age': patient.age,
                'gender': patient.gender,
                'height': patient.height,
                'weight': patient.weight,
                'created_at': patient.created_at.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/profile', methods=['PUT'])
@jwt_required()
@require_role('patient')
def update_profile():
    """
    Update patient's profile information
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'contact_number' in data:
            patient.contact_number = data['contact_number']
        if 'address' in data:
            patient.address = data['address']
        if 'age' in data:
            patient.age = data['age']
        if 'gender' in data:
            patient.gender = data['gender']
        if 'height' in data:
            patient.height = data['height']
        if 'weight' in data:
            patient.weight = data['weight']
        
        # Update user fields if provided
        if 'username' in data:
            patient.user.username = data['username']
        if 'email' in data:
            # Check if email already exists
            if User.query.filter(User.email == data['email'], User.id != current_user_id).first():
                return jsonify({'error': 'Email already in use'}), 400
            patient.user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Profile updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/doctors/available', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_available_doctors():
    """
    Get list of available doctors for the next 7 days
    Optional query parameter: specialization (to filter by specialization)
    """
    try:
        specialization = request.args.get('specialization', '').strip()
        
        query = Doctor.query.filter(Doctor.is_blacklisted == False)
        
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
        
        doctors = query.all()
        
        doctors_list = []
        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'name': doctor.user.username,
                'email': doctor.user.email,
                'specialization': doctor.specialization,
                'availability': json.loads(doctor.availability) if doctor.availability else {}
            }
            doctors_list.append(doctor_data)
        
        return jsonify({
            'status': 'success',
            'doctors': doctors_list,
            'count': len(doctors_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/appointments/book', methods=['POST'])
@jwt_required()
@require_role('patient')
def book_appointment():
    """
    Book an appointment with a doctor
    Required fields: doctor_id, date, time
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['doctor_id', 'date', 'time']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if doctor exists
        doctor = Doctor.query.get(data['doctor_id'])
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        if doctor.is_blacklisted:
            return jsonify({'error': 'Doctor is not available'}), 400
        
        # Check for conflicting appointments
        existing_appointment = Appointment.query.filter(
            Appointment.doctor_id == data['doctor_id'],
            Appointment.date == data['date'],
            Appointment.time == data['time'],
            Appointment.status != 'Cancelled'
        ).first()
        
        if existing_appointment:
            return jsonify({'error': 'This time slot is already booked'}), 400
        
        # Create appointment
        appointment = Appointment(
            doctor_id=data['doctor_id'],
            patient_id=patient.id,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M').time(),
            status='Booked'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment booked successfully',
            'appointment': {
                'id': appointment.id,
                'doctor_name': doctor.user.username,
                'specialization': doctor.specialization,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid date or time format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/appointments/<int:appointment_id>/reschedule', methods=['POST'])
@jwt_required()
@require_role('patient')
def reschedule_appointment(appointment_id):
    """
    Reschedule an appointment to a different date/time
    Required fields: date, time
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.patient_id != patient.id:
            return jsonify({'error': 'Not authorized to reschedule this appointment'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        if 'date' not in data or 'time' not in data:
            return jsonify({'error': 'Date and time are required'}), 400
        
        # Check for conflicting appointments
        existing_appointment = Appointment.query.filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.date == datetime.strptime(data['date'], '%Y-%m-%d').date(),
            Appointment.time == datetime.strptime(data['time'], '%H:%M').time(),
            Appointment.status != 'Cancelled',
            Appointment.id != appointment_id
        ).first()
        
        if existing_appointment:
            return jsonify({'error': 'This time slot is already booked'}), 400
        
        appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        appointment.time = datetime.strptime(data['time'], '%H:%M').time()
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment rescheduled successfully',
            'appointment': {
                'id': appointment.id,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date or time format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
@require_role('patient')
def cancel_appointment(appointment_id):
    """
    Cancel an appointment
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.patient_id != patient.id:
            return jsonify({'error': 'Not authorized to cancel this appointment'}), 403
        
        appointment.status = 'Cancelled'
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment cancelled successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/appointments', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_appointments():
    """
    Get all appointments for the patient (upcoming and past)
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id
        ).order_by(Appointment.date.desc()).all()
        
        appointments_list = []
        for appointment in appointments:
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            appointment_data = {
                'id': appointment.id,
                'doctor_name': appointment.doctor.user.username,
                'specialization': appointment.doctor.specialization,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status,
                'diagnosis': treatment.diagnosis if treatment else None,
                'prescription': treatment.prescription if treatment else None,
                'notes': treatment.notes if treatment else None
            }
            appointments_list.append(appointment_data)
        
        return jsonify({
            'status': 'success',
            'appointments': appointments_list,
            'count': len(appointments_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/medical-history', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_medical_history():
    """
    Get complete medical history (completed appointments with diagnoses and prescriptions)
    """
    try:
        current_user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=current_user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        # Get all completed appointments
        completed_appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.date.desc()).all()
        
        history = []
        for appointment in completed_appointments:
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            history_data = {
                'appointment_id': appointment.id,
                'doctor_name': appointment.doctor.user.username,
                'specialization': appointment.doctor.specialization,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'diagnosis': treatment.diagnosis if treatment else None,
                'prescription': treatment.prescription if treatment else None,
                'notes': treatment.notes if treatment else None,
                'next_visit_suggested': treatment.next_visit_suggested.isoformat() if treatment and treatment.next_visit_suggested else None
            }
            history.append(history_data)
        
        return jsonify({
            'status': 'success',
            'patient': {
                'id': patient.id,
                'name': patient.user.username,
                'age': patient.age,
                'gender': patient.gender
            },
            'medical_history': history,
            'count': len(history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
