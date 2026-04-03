from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User (role: Admin/Doctor/Patient)
class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(80) , unique=True , nullable = False)
    email = db.Column(db.String(80) , unique= True , nullable = False)
    password_hash = db.Column(db.String(255) , nullable = False)
    role = db.Column(db.String(20) , nullable = False)  # 'admin', 'doctor', 'patient'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships:
    doctor = db.relationship('Doctor' , backref= 'user' , uselist= False)
    patient = db.relationship('Patient' , backref= 'user' , uselist= False) 


# Doctor class 
class Doctor(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(100) , nullable = False)
    availability = db.Column(db.String(50) , nullable = True)  # JSON string for availability
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships:
    appointments = db.relationship('Appointment' , backref = 'doctor')


    
# Patient Class 
class Patient(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    contact_number = db.Column(db.String(20) , nullable = False)
    address = db.Column(db.String(200) , nullable = True)
    age = db.Column(db.Integer , nullable = False)
    gender = db.Column(db.String(10) , nullable = False)
    height = db.Column(db.Float , nullable = False)
    weight = db.Column(db.Float , nullable = False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships:
    appointments = db.relationship('Appointment' , backref = 'patient')


# Appointment Class 
class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    doctor_id = db.Column(db.Integer , db.ForeignKey('doctor.id') , nullable = False)
    patient_id = db.Column(db.Integer , db.ForeignKey('patient.id') , nullable = False)
    date = db.Column(db.Date , nullable = False)
    time = db.Column(db.Time , nullable = False)
    status = db.Column(db.String(20) , default = 'Booked', nullable = False)  # 'Booked', 'Completed', 'Cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships:
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)


#Treatment Class
class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    next_visit_suggested = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Department Class 
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)      



