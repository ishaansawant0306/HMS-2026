"""
Celery Beat schedule configuration for periodic tasks
This defines when scheduled jobs should run
"""
from celery.schedules import crontab
from datetime import timedelta

# celery beat schedule config
CELERY_BEAT_SCHEDULE = {
    
    'send-daily-appointment-reminders': {
        'task': 'tasks.send_daily_appointment_reminders',
        'schedule': crontab(hour=2, minute=30),  
        'options': {'queue': 'default'}
    },
    
    # monthly reports 
    'generate-monthly-doctor-report': {
        'task': 'tasks.generate_monthly_doctor_report',
        'schedule': crontab(day_of_month=1, hour=3, minute=30), 
        'options': {'queue': 'default'}
    },
}


CELERY_CONFIG = {
    'CELERY_TIMEZONE': 'Asia/Kolkata',
    'CELERY_ENABLE_UTC': True,
}


CELERY_TASK_ROUTES = {
    'tasks.send_daily_appointment_reminders': {'queue': 'default'},
    'tasks.generate_monthly_doctor_report': {'queue': 'default'},
    'tasks.export_patient_treatment_history': {'queue': 'high'},
}
