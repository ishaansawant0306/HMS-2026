# Hospital Management System (HMS) - Milestone 2: Authentication & Role-Based Access

## Overview
This document describes the implementation of Milestone 2, which covers:
- Authentication system (JWT-based)
- Role-Based Access Control (RBAC) for Admin, Doctor, and Patient
- Separate routes and dashboards for each role
- Role-based redirections after login

## Architecture

### Authentication Flow
1. User provides email and password to `/api/auth/login`
2. System validates credentials and returns JWT token
3. Token includes user role and ID in claims
4. Frontend uses token and redirect URL to route to appropriate dashboard
5. Subsequent requests include token in Authorization header

### User Roles

#### Admin
- Pre-existing user created programmatically during app initialization
- Full access to manage doctors, patients, and appointments
- Can view all system statistics

#### Doctor
- Created only by Admin
- Can view their own appointments and patients
- Can mark appointments as completed with treatment notes
- Can set their availability

#### Patient
- Can self-register
- Can search for doctors and book appointments
- Can view their medical history
- Can cancel/reschedule appointments

## API Endpoints

### Authentication Routes (`/api/auth`)

#### Patient Registration
```
POST /api/auth/register/patient
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "age": 30,
  "gender": "Male",
  "contact_number": "+1234567890",
  "address": "123 Main St",  // optional
  "height": 5.9,  // optional
  "weight": 70.0  // optional
}

Response (201):
{
  "status": "success",
  "message": "Patient registered successfully",
  "patient": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Login (All Roles)
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response (200):
{
  "status": "success",
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "patient"
  },
  "redirect": "/api/patient/dashboard"
}
```

#### Get Current User
```
GET /api/auth/me
Authorization: Bearer <token>

Response (200):
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "patient",
    "is_active": true,
    "created_at": "2024-04-03T10:30:00"
  }
}
```

### Admin Routes (`/api/admin`)
All require: `Authorization: Bearer <admin_token>`

#### Admin Dashboard
```
GET /api/admin/dashboard

Response (200):
{
  "status": "success",
  "dashboard": {
    "total_doctors": 5,
    "total_patients": 20,
    "total_appointments": 45,
    "upcoming_appointments": 12
  }
}
```

#### Get All Doctors
```
GET /api/admin/doctors

Response (200):
{
  "status": "success",
  "doctors": [...],
  "count": 5
}
```

#### Add Doctor
```
POST /api/admin/doctors

{
  "username": "dr_smith",
  "email": "smith@hospital.com",
  "password": "password123",
  "specialization": "Cardiology",
  "availability": "{}"  // optional JSON string
}

Response (201): Created successfully
```

#### Update Doctor
```
PUT /api/admin/doctors/<doctor_id>

{
  "specialization": "Cardiology",
  "availability": "{}"
}
```

#### Blacklist Doctor
```
POST /api/admin/doctors/<doctor_id>/blacklist

Response (200): Blacklisted successfully
```

#### Get All Appointments
```
GET /api/admin/appointments

Response (200):
{
  "status": "success",
  "appointments": [...],
  "count": 45
}
```

#### Search Patients
```
GET /api/admin/search/patients?q=john

Response (200):
{
  "status": "success",
  "patients": [...],
  "count": 3
}
```

#### Search Doctors
```
GET /api/admin/search/doctors?q=cardiology

Response (200):
{
  "status": "success",
  "doctors": [...],
  "count": 2
}
```

#### Blacklist Patient
```
POST /api/admin/patients/<patient_id>/blacklist

Response (200): Blacklisted successfully
```

### Doctor Routes (`/api/doctor`)
All require: `Authorization: Bearer <doctor_token>`

#### Doctor Dashboard
```
GET /api/doctor/dashboard

Response (200):
{
  "status": "success",
  "doctor": {
    "name": "Dr. Smith",
    "specialization": "Cardiology",
    "upcoming_appointments_count": 5,
    "patients_count": 12
  },
  "appointments": [...],
  "patients": [...]
}
```

#### Get Doctor's Appointments
```
GET /api/doctor/appointments

Response (200):
{
  "status": "success",
  "appointments": [...],
  "count": 15
}
```

#### Complete Appointment with Treatment
```
POST /api/doctor/appointments/<appointment_id>/complete

{
  "diagnosis": "Hypertension",
  "prescription": "Lisinopril 10mg daily",
  "notes": "Follow-up in 1 month",
  "next_visit_suggested": "2024-05-03"  // optional
}

Response (200): Appointment marked as completed
```

#### Cancel Appointment
```
POST /api/doctor/appointments/<appointment_id>/cancel

Response (200): Appointment cancelled
```

#### Set Availability
```
POST /api/doctor/availability

{
  "availability": {
    "Monday": ["09:00-12:00", "14:00-17:00"],
    "Tuesday": ["09:00-12:00", "14:00-17:00"],
    ...
  }
}

Response (200): Availability updated
```

#### Get Patient History
```
GET /api/doctor/patient/<patient_id>/history

Response (200):
{
  "status": "success",
  "patient": {...},
  "history": [
    {
      "appointment_id": 1,
      "date": "2024-04-01",
      "time": "10:00:00",
      "diagnosis": "Hypertension",
      "prescription": "...",
      "notes": "...",
      "next_visit_suggested": "2024-05-03"
    }
  ],
  "count": 3
}
```

### Patient Routes (`/api/patient`)
All require: `Authorization: Bearer <patient_token>`

#### Patient Dashboard
```
GET /api/patient/dashboard

Response (200):
{
  "status": "success",
  "patient": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "gender": "Male"
  },
  "upcoming_appointments": [...],
  "upcoming_count": 2,
  "specializations": ["Cardiology", "Orthopedics", ...]
}
```

#### Get Patient Profile
```
GET /api/patient/profile

Response (200):
{
  "status": "success",
  "patient": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "contact_number": "+1234567890",
    "address": "123 Main St",
    "age": 30,
    "gender": "Male",
    "height": 5.9,
    "weight": 70.0,
    "created_at": "2024-04-03T10:30:00"
  }
}
```

#### Update Patient Profile
```
PUT /api/patient/profile

{
  "contact_number": "+9876543210",
  "address": "456 Oak Ave",
  "age": 31,
  "height": 5.9,
  "weight": 71.0
}

Response (200): Profile updated
```

#### Get Available Doctors
```
GET /api/patient/doctors/available?specialization=Cardiology

Response (200):
{
  "status": "success",
  "doctors": [
    {
      "id": 1,
      "name": "Dr. Smith",
      "email": "smith@hospital.com",
      "specialization": "Cardiology",
      "availability": {...}
    }
  ],
  "count": 3
}
```

#### Book Appointment
```
POST /api/patient/appointments/book

{
  "doctor_id": 1,
  "date": "2024-04-10",
  "time": "14:00"
}

Response (201):
{
  "status": "success",
  "message": "Appointment booked successfully",
  "appointment": {
    "id": 5,
    "doctor_name": "Dr. Smith",
    "specialization": "Cardiology",
    "date": "2024-04-10",
    "time": "14:00",
    "status": "Booked"
  }
}
```

#### Reschedule Appointment
```
POST /api/patient/appointments/<appointment_id>/reschedule

{
  "date": "2024-04-15",
  "time": "10:00"
}

Response (200): Appointment rescheduled
```

#### Cancel Appointment
```
POST /api/patient/appointments/<appointment_id>/cancel

Response (200): Appointment cancelled
```

#### Get All Appointments
```
GET /api/patient/appointments

Response (200):
{
  "status": "success",
  "appointments": [...],
  "count": 8
}
```

#### Get Medical History
```
GET /api/patient/medical-history

Response (200):
{
  "status": "success",
  "patient": {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "gender": "Male"
  },
  "medical_history": [
    {
      "appointment_id": 1,
      "doctor_name": "Dr. Smith",
      "specialization": "Cardiology",
      "date": "2024-04-01",
      "time": "10:00",
      "diagnosis": "Hypertension",
      "prescription": "Lisinopril 10mg daily",
      "notes": "Follow-up in 1 month",
      "next_visit_suggested": "2024-05-03"
    }
  ],
  "count": 3
}
```

## Security Features

1. **JWT Authentication**: All protected endpoints require valid JWT token
2. **Role-Based Access Control**: `@require_role()` decorator enforces role-based access
3. **Password Hashing**: All passwords hashed using PBKDF2-SHA256
4. **Token Claims**: JWT includes user ID and role for quick authorization
5. **User Validation**: Each request validates user existence and active status

## Testing the API

### 1. Initialize Admin
The admin user is created automatically when the app starts:
- Username: `admin`
- Email: `admin@hospital.com`
- Password: `admin123`

### 2. Register a Patient
```bash
curl -X POST http://localhost:5000/api/auth/register/patient \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "age": 30,
    "gender": "Male",
    "contact_number": "+1234567890"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 4. Access Protected Endpoint
```bash
curl -X GET http://localhost:5000/api/patient/dashboard \
  -H "Authorization: Bearer <access_token>"
```

## File Structure
```
Backend/
├── app.py                 # Flask app creation and initialization
├── models.py              # SQLAlchemy models
├── init_db.py             # Admin initialization
├── requirements.txt       # Python dependencies
├── routes/
│   ├── __init__.py        # Blueprint registration
│   ├── auth.py            # Authentication endpoints
│   ├── admin.py           # Admin-specific routes
│   ├── doctor.py          # Doctor-specific routes
│   └── patient.py         # Patient-specific routes
└── utils/
    └── auth.py            # Authorization utilities and decorators
```

## Middleware & Utilities

### `require_role(*allowed_roles)`
Decorator that ensures only users with specified roles can access an endpoint.

### `hash_password(password)`
Hashes a password using PBKDF2-SHA256.

### `verify_password(hashed_password, password)`
Verifies a password against its hash.

## Next Steps (Milestone 3+)
- Frontend implementation with Vue.js
- Real-time notifications
- Appointment reminder system
- Advanced search and filtering
- Doctor availability calendar
- Patient health records management
- Admin reports and analytics
