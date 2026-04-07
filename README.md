# Hospital Management System (HMS) - Version 2.0

A modern, role-based Hospital Management System web application built with Flask, Vue.js, and SQLite. Designed to streamline hospital operations by managing patients, doctors, appointments, and treatments efficiently.

## 🎯 Features

### Admin Dashboard
- **Dashboard Statistics**: View total doctors, patients, and appointments breakdown
- **Doctor Management**: Add, edit, delete, and blacklist doctors
- **Patient Management**: Search and manage patient records
- **Appointment Oversight**: View all appointments (upcoming and past)
- **Search Functionality**: Search patients by name/email and doctors by specialization

### Doctor Dashboard
- **Appointment Management**: View and manage upcoming appointments
- **Patient Treatment Records**: Add diagnosis, prescriptions, and treatment notes
- **Patient History**: Access complete medical history of patients
- **Availability Settings**: Set weekly availability schedule
- **Assigned Patients**: View list of assigned patients

### Patient Dashboard
- **Profile Management**: Register, login, and update personal information
- **Doctor Search**: Browse available doctors by specialization
- **Appointment Booking**: Book, reschedule, or cancel appointments
- **Medical History**: View past appointments with treatment details
- **Appointment Status**: Track upcoming appointments in real-time

### Background Jobs (Celery + Redis)
- **Daily Reminders**: Automated appointment reminders via email
- **Monthly Reports**: Generate monthly activity reports for doctors
- **CSV Export**: Patient treatment history export (async job)

## 🛠 Technology Stack

- **Backend**: Flask 3.1.2, SQLAlchemy 2.0.44
- **Frontend**: Vue.js 3, Vue Router 4, Axios
- **Database**: SQLite
- **Authentication**: JWT (Flask-JWT-Extended)
- **Background Jobs**: Celery + Redis
- **API Communication**: RESTful with CORS support
- **Styling**: CSS3 with responsive design

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- Redis (for Celery jobs)
- SQLite3 (usually pre-installed)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hms-2026.git
cd HMS-2026
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

#### Configure Environment (Optional)
Create a `.env` file in the Backend directory:
```env
FLASK_ENV=development
JWT_SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///hms2026.db
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
```

#### Initialize Database
```bash
python init_db.py
```

This creates the database and adds:
- **Admin User**: `admin` / `admin@hospital.com` / `admin123`
- **Test Doctor**: `testdoctor` / `testdoctor@hospital.com` / `doctor123`

#### Run Flask Server
```bash
python app.py
```

Backend runs on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` (Vite) or `http://localhost:8080` (if configured)

### 4. Redis Setup (For Background Jobs)

#### Windows
Download and install from: https://github.com/microsoftarchive/redis/releases

Or use Windows Subsystem for Linux (WSL):
```bash
wsl redis-server
```

#### Linux/macOS
```bash
brew install redis  # macOS
sudo apt-get install redis-server  # Ubuntu/Debian
redis-server
```

### 5. Celery Worker (Optional - For Background Jobs)

In a new terminal:
```bash
cd Backend
celery -A tasks worker --loglevel=info
```

## 📖 Usage

### Admin Access
1. Navigate to `http://localhost:5173/login`
2. Login with credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Access admin dashboard for doctor/patient management

### Doctor Access
1. Admin must add a doctor first
2. Navigate to `http://localhost:5173/login`
3. Login with doctor credentials (provided by admin)
4. Access doctor dashboard to manage appointments and treatments

### Patient Access
1. Navigate to `http://localhost:5173/register`
2. Create a new patient account
3. Login and access patient dashboard
4. Search for doctors and book appointments

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/patient` - Patient registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Admin Routes
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/doctors` - List all doctors
- `POST /api/admin/doctors` - Create new doctor
- `PUT /api/admin/doctors/<id>` - Update doctor
- `DELETE /api/admin/doctors/<id>` - Delete doctor
- `POST /api/admin/doctors/<id>/blacklist` - Blacklist doctor
- `GET /api/admin/patients` - List all patients
- `GET /api/admin/appointments` - View all appointments
- `GET /api/admin/search/patients` - Search patients
- `GET /api/admin/search/doctors` - Search doctors

### Doctor Routes
- `GET /api/doctor/dashboard` - Doctor dashboard
- `GET /api/doctor/appointments` - List appointments
- `POST /api/doctor/appointments/<id>/complete` - Mark appointment complete & add treatment
- `POST /api/doctor/appointments/<id>/cancel` - Cancel appointment
- `POST /api/doctor/availability` - Set weekly availability
- `GET /api/doctor/patient/<id>/history` - Get patient medical history

### Patient Routes
- `GET /api/patient/dashboard` - Patient dashboard
- `GET /api/patient/profile` - Get patient profile
- `PUT /api/patient/profile` - Update patient profile
- `GET /api/patient/doctors/available` - List available doctors
- `GET /api/patient/appointments` - Get all patient appointments
- `POST /api/patient/appointments/book` - Book appointment
- `POST /api/patient/appointments/<id>/reschedule` - Reschedule appointment
- `POST /api/patient/appointments/<id>/cancel` - Cancel appointment
- `GET /api/patient/medical-history` - Get medical history

## 📁 Project Structure

```
HMS-2026/
├── Backend/
│   ├── app.py                  # Flask application entry point
│   ├── models.py               # Database models
│   ├── init_db.py              # Database initialization
│   ├── requirements.txt         # Python dependencies
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   ├── admin.py           # Admin routes
│   │   ├── doctor.py          # Doctor routes
│   │   └── patient.py         # Patient routes
│   ├── utils/
│   │   └── auth.py            # Authentication utilities
│   ├── tasks/                 # Celery tasks (background jobs)
│   └── instance/              # Database file location
│
├── Frontend/
│   ├── src/
│   │   ├── App.vue            # Root Vue component
│   │   ├── main.js            # Vue app entry point
│   │   ├── style.css          # Global styles
│   │   ├── components/
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── DoctorDashboard.vue
│   │   │   └── PatientDashboard.vue
│   │   └── router/
│   │       └── index.js       # Route configuration
│   ├── package.json           # Node depend encies
│   ├── vite.config.js         # Vite configuration
│   └── index.html             # HTML entry point
│
├── .gitignore
├── README.md
└── start-dev.ps1              # Development startup script (Windows)
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: PBKDF2:SHA256 with salt
- **Role-Based Access Control**: Admin, Doctor, Patient roles with specific permissions
- **CORS Protection**: Restricted to allowed origins
- **Token Expiration**: 1-hour access tokens, 30-day refresh tokens
- **Input Validation**: Server-side validation on all endpoints

## 📝 Database Schema

### User Table
- Role-based user management (admin, doctor, patient)
- Password hashing and authentication

### Doctor Table
- Specialization and availability management
- Blacklist status for soft deletion

### Patient Table
- Patient profile information
- Contact details and medical information

### Appointment Table
- Doctor-Patient linkage
- Date, time, and status tracking
- Supports: Booked, Completed, Cancelled statuses

### Treatment Table
- Appointment-linked treatment records
- Diagnosis, prescriptions, and notes

### Department Table
- Medical specializations management

## 🎓 Development Notes

### Adding New Features
1. Create API endpoint in `Backend/routes/`
2. Add corresponding Vue component/method in `Frontend/src/components/`
3. Use axios to call the API with JWT token from localStorage
4. Handle responses and update component state

### Running Tests
```bash
# Backend tests (if implemented)
pytest Backend/tests/

# Frontend tests (if implemented)
npm run test --prefix Frontend
```

### Debugging
- **Backend**: Check Flask logs in terminal
- **Frontend**: Use browser DevTools console and Network tab
- **Database**: Use `sqlite3 hms2026.db` to inspect

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/new-feature`
2. Make your changes and commit: `git commit -m 'Add new feature'`
3. Push to branch: `git push origin feature/new-feature`
4. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### CORS Errors
- Ensure backend is running on `http://localhost:5000`
- Check CORS configuration in `app.py`

### Database Errors
- Delete `hms2026.db` and run `python init_db.py` again
- Ensure no other process is using the database

### Token Expired
- Frontend automatically handles 401 errors by redirecting to login
- Clear localStorage and login again

### Celery Not Working
- Ensure Redis is running: `redis-server`
- Check Celery worker logs for errors

## 📞 Support

For issues or questions, please refer to the documentation or create an issue in the repository.

---

**Version**: 2.0  
**Last Updated**: April 2026  
**Status**: Active Development
