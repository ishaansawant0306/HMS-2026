"""
Celery Beat schedule configuration for periodic tasks
This defines when scheduled jobs should run
"""
from celery.schedules import crontab
from datetime import timedelta

# Celery Beat Schedule Configuration
CELERY_BEAT_SCHEDULE = {
    # Daily reminders - Run every day at 8:00 AM IST (02:30 UTC)
    'send-daily-appointment-reminders': {
        'task': 'tasks.send_daily_appointment_reminders',
        'schedule': crontab(hour=2, minute=30),  # 8:00 AM IST
        'options': {'queue': 'default'}
    },
    
    # Monthly reports - Run on the 1st of every month at 9:00 AM IST (03:30 UTC)
    'generate-monthly-doctor-report': {
        'task': 'tasks.generate_monthly_doctor_report',
        'schedule': crontab(day_of_month=1, hour=3, minute=30),  # 1st, 9:00 AM IST
        'options': {'queue': 'default'}
    },
}

# Additional Celery configuration
CELERY_CONFIG = {
    'CELERY_TIMEZONE': 'Asia/Kolkata',
    'CELERY_ENABLE_UTC': True,
}

# Task routing (optional)
CELERY_TASK_ROUTES = {
    'tasks.send_daily_appointment_reminders': {'queue': 'default'},
    'tasks.generate_monthly_doctor_report': {'queue': 'default'},
    'tasks.export_patient_treatment_history': {'queue': 'high'},
}
