"""
Celery tasks for HMS background jobs
- Daily appointment reminders
- Monthly doctor activity reports
- CSV export of patient treatment history
"""
import os
import csv
import requests
from celery import shared_task
from datetime import datetime, timedelta
from flask_mail import Message
from models import db, Appointment, Patient, Doctor, Treatment, User
from extensions import mail

NOTIFICATION_WEBHOOK_URL = os.getenv('NOTIFICATION_WEBHOOK_URL')
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exports')
os.makedirs(EXPORTS_DIR, exist_ok=True)

# Note: Configure Flask-Mail in your app.py for email functionality

# ============================================================================
# TASK 1: DAILY APPOINTMENT REMINDERS
# ============================================================================

@shared_task
def send_daily_appointment_reminders():
    """
    Send reminders to patients about appointments scheduled for today
    Runs daily at a scheduled time (configured in Celery Beat)
    """
    try:
        today = datetime.now().date()
        
        # Find all appointments scheduled for today
        appointments = Appointment.query.filter(
            Appointment.date == today,
            Appointment.status == 'Booked'
        ).all()
        
        reminder_count = 0
        
        for appointment in appointments:
            patient_email = appointment.patient.user.email
            patient_name = appointment.patient.user.username
            doctor_name = appointment.doctor.user.username
            reminder_time = appointment.time.strftime("%H:%M")
            
            try:
                subject = "Appointment Reminder - MediZentrum"
                body = f"""
Dear {patient_name},

This is a reminder about your appointment scheduled today with Dr. {doctor_name}.

Appointment Details:
- Time: {reminder_time}
- Doctor: Dr. {doctor_name}
- Specialization: {appointment.doctor.specialization}

Please arrive 10 minutes before the scheduled time.

If you need to cancel or reschedule, please log in to your MediZentrum account.

Best regards,
MediZentrum Hospital Management System
                """

                send_notification(
                    recipient_email=patient_email,
                    subject=subject,
                    body=body,
                    webhook_payload={
                        'text': f"REMINDER: Dear {patient_name}, you have an appointment today at {reminder_time} with Dr. {doctor_name}."
                    }
                )
                reminder_count += 1
                print(f"Reminder triggered for {patient_email} at {reminder_time}")
            except Exception as e:
                print(f"Failed to trigger reminder for {patient_email}: {str(e)}")
        
        return {
            'status': 'success',
            'reminders_sent': reminder_count,
            'date': str(today)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


# ============================================================================
# TASK 2: MONTHLY DOCTOR ACTIVITY REPORT
# ============================================================================

@shared_task
def generate_monthly_doctor_report(doctor_id=None, month=None, year=None):
    """
    Generate monthly activity report for doctor(s)
    Includes: appointments, diagnoses, treatments provided
    Typically run on the 1st of each month
    """
    try:
        # Default to previous month if not specified
        if not month or not year:
            today = datetime.now().date()
            if today.month == 1:
                year = today.year - 1
                month = 12
            else:
                year = today.year
                month = today.month - 1
        
        # Get doctors to generate reports for
        if doctor_id:
            doctors = [Doctor.query.get(doctor_id)]
        else:
            doctors = Doctor.query.filter(Doctor.is_blacklisted == False).all()
        
        reports_generated = 0
        
        for doctor in doctors:
            if not doctor:
                continue
            
            doctor_email = doctor.user.email
            doctor_name = doctor.user.username
            
            # Get all completed appointments for the month
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.status == 'Completed',
                Appointment.date >= datetime(year, month, 1).date(),
                Appointment.date < datetime(year, month + 1, 1).date() if month < 12 else datetime(year + 1, 1, 1).date()
            ).all()
            
            if not appointments:
                continue
            
            # Build report
            report_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #2f80ed; color: white; padding: 20px; }}
                    .content {{ padding: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f8f9fb; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Monthly Activity Report</h1>
                    <p>Dr. {doctor_name} - {month}/{year}</p>
                </div>
                <div class="content">
                    <h2>Summary</h2>
                    <p><strong>Total Appointments:</strong> {len(appointments)}</p>
                    <p><strong>Doctor:</strong> Dr. {doctor_name}</p>
                    <p><strong>Specialization:</strong> {doctor.specialization}</p>
                    
                    <h2>Appointment Details</h2>
                    <table>
                        <tr>
                            <th>Date</th>
                            <th>Patient Name</th>
                            <th>Diagnosis</th>
                            <th>Treatment</th>
                        </tr>
            """
            
            # Add appointment details
            for appointment in appointments:
                treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
                diagnosis = treatment.diagnosis if treatment else "N/A"
                treatment_text = treatment.prescription if treatment else "N/A"
                
                report_html += f"""
                        <tr>
                            <td>{appointment.date}</td>
                            <td>{appointment.patient.user.username}</td>
                            <td>{diagnosis}</td>
                            <td>{treatment_text}</td>
                        </tr>
                """
            
            report_html += """
                    </table>
                    <footer style="margin-top: 20px; font-size: 12px; color: #999;">
                        <p>This is an automated report generated by MediZentrum</p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            # Save HTML file locally since emails are dummy
            filename = f"monthly_report_{doctor_name.replace(' ', '_')}_{month}_{year}.html"
            filepath = os.path.join(EXPORTS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_html)
            
            try:
                subject = f"Monthly Activity Report - {month}/{year}"
                send_notification(
                    recipient_email=doctor_email,
                    subject=subject,
                    body=f"Dear Dr. {doctor_name},\n\nYour activity report for {month}/{year} has been generated and saved locally to {filepath}.",
                    html=report_html,
                    webhook_payload={
                        'text': f"MONTHLY REPORT: Activity report for Dr. {doctor_name} physically saved to {filepath}"
                    }
                )
                reports_generated += 1
                print(f"Monthly report triggered for {doctor_email} for {month}/{year}")
            except Exception as e:
                print(f"Failed to trigger report for {doctor_email}: {str(e)}")
        
        return {
            'status': 'success',
            'reports_generated': reports_generated,
            'month': month,
            'year': year
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


# ============================================================================
# TASK 3: CSV EXPORT OF PATIENT TREATMENT HISTORY
# ============================================================================

@shared_task
def export_patient_treatment_history(patient_id):
    """
    Generate CSV export of patient's complete treatment history
    Returns file path or download URL
    """
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return {
                'status': 'error',
                'error': 'Patient not found'
            }
        
        # Get all completed appointments with treatments
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient_id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.date.desc()).all()
        
        # Generate CSV data
        csv_data = []
        headers = [
            'User ID', 'Username', 'Consulting Doctor', 'Appointment Date',
            'Diagnosis Given', 'Treatment Given', 'Next Visit Suggested', 'Status'
        ]
        csv_data.append(headers)
        
        for appointment in appointments:
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            
            row = [
                str(patient.user.id),
                patient.user.username,
                f"Dr. {appointment.doctor.user.username}",
                str(appointment.date),
                treatment.diagnosis if treatment else "N/A",
                treatment.prescription if treatment else "N/A",
                str(treatment.next_visit_suggested) if treatment and treatment.next_visit_suggested else "N/A",
                appointment.status
            ]
            csv_data.append(row)
        
        # Create CSV file
        filename = f"treatment_history_{patient.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(EXPORTS_DIR, filename)
        
        # Write CSV
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(csv_data)
            
            patient_email = patient.user.email
            subject = "Your Treatment History Export - MediZentrum"
            body = f"""
Dear {patient.user.username},

Your treatment history has been successfully exported and is ready for download.

File: {filename}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Records: {len(appointments)}

Please check your notifications or contact support if you do not see the download link.

Best regards,
MediZentrum Hospital Management System
                """
            send_notification(
                recipient_email=patient_email,
                subject=subject,
                body=body,
                webhook_payload={
                    'type': 'treatment_history_export',
                    'patient_email': patient_email,
                    'patient_id': patient_id,
                    'filename': filename,
                    'filepath': filepath,
                    'records_exported': len(appointments)
                }
            )
            
            return {
                'status': 'success',
                'filename': filename,
                'filepath': filepath,
                'records_exported': len(appointments),
                'generated_at': str(datetime.now())
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Failed to create CSV: {str(e)}"
            }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def send_notification(recipient_email, subject, body, html=None, webhook_payload=None):
    """Send a notification by email first, then fallback to webhook if configured."""
    sent = False
    if mail:
        try:
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body,
                html=html
            )
            mail.send(msg)
            sent = True
            print(f"Notification email sent to {recipient_email}")
        except Exception as e:
            print(f"Email send failed for {recipient_email}: {str(e)}")

    if not sent and NOTIFICATION_WEBHOOK_URL:
        sent = send_via_webhook(webhook_payload or {
            'type': 'notification',
            'recipient_email': recipient_email,
            'subject': subject,
            'body': body
        })

    if not sent:
        print(f"Notification fallback: no email or webhook configured for {recipient_email}")

    return sent


def send_via_webhook(payload):
    """Send a webhook notification mapped specifically for Google Chat natively."""
    if not NOTIFICATION_WEBHOOK_URL:
        return False

    try:
        # Standardize for Google Chat integration
        chat_payload = {"text": payload.get('text', str(payload))}
        
        response = requests.post(NOTIFICATION_WEBHOOK_URL, json=chat_payload, timeout=10)
        response.raise_for_status()
        print(f"Webhook notification sent to Google Chat.")
        return True
    except Exception as e:
        print(f"Webhook notification failed: {str(e)}")
        return False
