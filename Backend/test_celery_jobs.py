"""
test_celery_jobs.py
Run this to manually test all 3 background jobs right now.
Does NOT require Celery or Redis - calls tasks directly.
"""
from dotenv import load_dotenv
load_dotenv()

from app import app

with app.app_context():
    # Import the actual task functions (called directly, not via .delay())
    from tasks import (
        send_daily_appointment_reminders,
        generate_monthly_doctor_report
    )

    print("=" * 50)
    print("Testing Daily Appointment Reminder (Google Chat)")
    print("=" * 50)
    result = send_daily_appointment_reminders()
    print("Result:", result)
    print()

    print("=" * 50)
    print("Testing Monthly Doctor Report (HTML to disk)")
    print("=" * 50)
    result = generate_monthly_doctor_report()
    print("Result:", result)
    print()

    print("Done. Check your Google Chat Space for the daily reminder alert!")
    print("Check Backend/exports/ folder for the monthly HTML report file.")
