# test_celery_jobs.py
# Use this script to manually trigger your Daily and Monthly jobs for your Viva demonstration!

import os
from celery_config import celery_app
from tasks import send_daily_appointment_reminders, generate_monthly_doctor_report

def run_demonstration():
    print("======================================================")
    print("Triggering Viva Demonstration for Background Jobs")
    print("======================================================\n")

    print("[1] Dispatching Daily Reminders (Google Chat Webhook)...")
    try:
        send_daily_appointment_reminders.delay()
        print(" -> Task queued successfully! Check your Google Chat.\n")
    except Exception as e:
        print(f" -> Celery connection failed: {e}\n")

    print("[2] Dispatching Monthly Doctor Report Generation...")
    try:
        generate_monthly_doctor_report.delay()
        print(" -> Task queued successfully! Check your 'Backend/exports' folder for the HTML file.\n")
    except Exception as e:
        print(f" -> Celery connection failed: {e}\n")
        
    print("Demonstration tasks dispatched.")

if __name__ == "__main__":
    # Ensure app context is loaded if relying on SQLAlchemy implicitly
    from app import app
    with app.app_context():
        run_demonstration()
