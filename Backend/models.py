from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User (role: Admin/Doctor/Patient)
class User(db.Model):
    id = db.Column(db.Integer , primary_key=True) #--> primary key means ??
    username = db.Column(db.String(80) , unique=True , nullable = False)
    email = db.Column(db.String(80) , unique= True , nullable = False)
    password = db.Column(db.String(80) , nullable = False)
    role = db.Column(db.String(80) , nullable = False) 

    # Relationships:
    doctor = db.relationship('Doctor' , backref= 'user' , uselist= False)
    patient = db.relationship('Patient' , backref= 'user' , uselist= False) 


# Doctor class 
class Doctor(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(50) , nullable = False)
    availability = db.Column(db.String(50) , nullable = True)

    #Relationships:
    appointments = db.relationship('Appointment' , backref = 'doctor')


    
# Patient Class 
class Patient(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    contact_number = db.Column(db.Integer , nullable = False)
    address = db.Column(db.String(200) , nullable = True)
    age = db.Column(db.Integer , nullable = False)
    gender = db.Column(db.String(50) , nullable = False)
    height = db.Column(db.Integer , nullable = False)
    weight = db.Column(db.Integer , nullable = False)

    #Relationships:
    appointments = db.relationship('Appointment' , backref = 'patient')


# Appointment Class 
class Appointment(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    doctor_id = db.Column(db.Integer , db.ForeignKey('doctor.id') , nullable = False)
    patient_id = db.Column(db.Integer , db.ForeignKey('patient.id') , nullable = False)
    date = db.Column(db.Date , nullable = False)
    time = db.Column(db.Time , nullable = False)
    status = db.Column(db.String(50) , default = 'Booked')

 # Relationships:
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)


#Treatment Class
class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)


# Department Class 
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)      



