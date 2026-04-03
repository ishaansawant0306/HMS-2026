"""
Doctor routes for Hospital Management System
Handle doctor-specific operations like viewing appointments, updating treatment, etc.
"""
from flask import Blueprint, request, jsonify
from models import db, User, Doctor, Patient, Appointment, Treatment
from utils.auth import require_role
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
import json

doctor_bp = Blueprint('doctor', __name__, url_prefix='/api/doctor')


@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('doctor')
def dashboard():
    """
    Doctor dashboard - shows upcoming appointments and patient list
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Get doctor profile
        user = User.query.get(current_user_id)
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        # Get upcoming appointments for today and this week
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        
        upcoming_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date.between(today, week_end),
            Appointment.status.in_(['Booked', 'Completed'])
        ).all()
        
        # Get all patients assigned to this doctor
        patients = db.session.query(Patient).join(Appointment).filter(
            Appointment.doctor_id == doctor.id
        ).distinct().all()
        
        appointments_list = []
        for appointment in upcoming_appointments:
            appointment_data = {
                'id': appointment.id,
                'patient_name': appointment.patient.user.username,
                'patient_email': appointment.patient.user.email,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status,
                'contact_number': appointment.patient.contact_number
            }
            appointments_list.append(appointment_data)
        
        patients_list = []
        for patient in patients:
            patient_data = {
                'id': patient.id,
                'name': patient.user.username,
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender,
                'contact_number': patient.contact_number
            }
            patients_list.append(patient_data)
        
        return jsonify({
            'status': 'success',
            'doctor': {
                'name': doctor.user.username,
                'specialization': doctor.specialization,
                'upcoming_appointments_count': len(appointments_list),
                'patients_count': len(patients_list)
            },
            'appointments': appointments_list,
            'patients': patients_list
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
@require_role('doctor')
def get_appointments():
    """
    Get all appointments for the doctor
    """
    try:
        current_user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id
        ).all()
        
        appointments_list = []
        for appointment in appointments:
            appointment_data = {
                'id': appointment.id,
                'patient_name': appointment.patient.user.username,
                'patient_email': appointment.patient.user.email,
                'date': appointment.date.isoformat(),
                'time': appointment.time.isoformat(),
                'status': appointment.status,
                'contact_number': appointment.patient.contact_number,
                'created_at': appointment.created_at.isoformat()
            }
            appointments_list.append(appointment_data)
        
        return jsonify({
            'status': 'success',
            'appointments': appointments_list,
            'count': len(appointments_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/appointments/<int:appointment_id>/complete', methods=['POST'])
@jwt_required()
@require_role('doctor')
def complete_appointment(appointment_id):
    """
    Mark an appointment as completed and optionally add treatment details
    """
    try:
        current_user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.doctor_id != doctor.id:
            return jsonify({'error': 'Not authorized to update this appointment'}), 403
        
        appointment.status = 'Completed'
        
        # Add treatment details if provided
        data = request.get_json()
        if data and ('diagnosis' in data or 'prescription' in data or 'notes' in data):
            treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
            
            if not treatment:
                treatment = Treatment(appointment_id=appointment_id)
            
            treatment.diagnosis = data.get('diagnosis')
            treatment.prescription = data.get('prescription')
            treatment.notes = data.get('notes')
            treatment.next_visit_suggested = data.get('next_visit_suggested')
            
            db.session.add(treatment)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment marked as completed'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
@require_role('doctor')
def cancel_appointment(appointment_id):
    """
    Cancel an appointment
    """
    try:
        current_user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        if appointment.doctor_id != doctor.id:
            return jsonify({'error': 'Not authorized to cancel this appointment'}), 403
        
        appointment.status = 'Cancelled'
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Appointment cancelled'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/availability', methods=['POST'])
@jwt_required()
@require_role('doctor')
def set_availability():
    """
    Set doctor's availability for the next 7 days
    Expected JSON: {'availability': {'Monday': ['09:00-12:00', '14:00-17:00'], ...}}
    """
    try:
        current_user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        data = request.get_json()
        if 'availability' not in data:
            return jsonify({'error': 'Availability data required'}), 400
        
        # Store availability as JSON string
        doctor.availability = json.dumps(data['availability'])
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Availability updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/patient/<int:patient_id>/history', methods=['GET'])
@jwt_required()
@require_role('doctor')
def get_patient_history(patient_id):
    """
    Get treatment history for a specific patient
    """
    try:
        current_user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=current_user_id).first()
        
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get all completed appointments for this patient with this doctor
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient_id,
            Appointment.doctor_id == doctor.id,
            Appointment.status == 'Completed'
        ).all()
        
        history = []
        for appointment in appointments:
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            history_data = {
                'appointment_id': appointment.id,
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
                'email': patient.user.email,
                'age': patient.age,
                'gender': patient.gender
            },
            'history': history,
            'count': len(history)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
