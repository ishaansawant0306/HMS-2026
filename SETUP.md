# HMS-2026 Development Setup Guide

Quick-start guide for developers to set up and run the HMS application locally.

## Prerequisites

Before starting, ensure you have installed:
- Python 3.8+
- Node.js 14+ with npm
- Redis server
- Git

## Quick Start (5 minutes)

### 1️⃣ Windows - Using PowerShell Start Script

```powershell
# Navigate to project root
cd HMS-2026

# Run the provided startup script
.\start-dev.ps1
```

This will automatically:
- Activate Python virtual environment
- Start Redis
- Start Flask backend
- Start Vue frontend with Vite

### 2️⃣ Manual Setup (Linux/macOS/Windows)

#### Step 1: Backend Setup
```bash
# Navigate to backend
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env example (update with your values)
cp .env.example .env

# Initialize database
python init_db.py

# Start Flask server
python app.py
```

Backend runs on: **http://localhost:5000**

#### Step 2: Frontend Setup (New Terminal)
```bash
# Navigate to frontend
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

#### Step 3: Redis Setup (New Terminal)

**macOS:**
```bash
# Install Redis
brew install redis

# Start Redis server
brew services start redis
```

**Windows (WSL):**
```bash
# In WSL terminal
wsl redis-server
```

**Linux:**
```bash
sudo systemctl start redis-server
```

If using Docker:
```bash
docker run -d -p 6379:6379 redis:latest
```

#### Step 4: Celery Worker (Optional, New Terminal)
For background jobs (reminders, reports, exports):

```bash
cd Backend

# Activate venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Celery worker
celery -A tasks worker --loglevel=info
```

#### Step 5: Celery Beat (Optional, New Terminal)
For scheduled tasks:

```bash
cd Backend

# Activate venv
source venv/bin/activate

# Start Celery beat scheduler
celery -A tasks beat --loglevel=info
```

## 🔐 First Login

Once everything is running, open **http://localhost:5173**

### Default Credentials:

#### Admin Account:
- **Username**: `admin`
- **Password**: `admin123`

#### Test Doctor Account:
- **Username**: `testdoctor`
- **Password**: `doctor123`

#### Create Patient Account:
- Click "Register" and create a new account

## 📁 Project Structure

```
HMS-2026/
├── Backend/              # Flask API
│   ├── app.py           # Main app entry
│   ├── models.py        # Database models
│   ├── routes/          # API endpoints
│   ├── tasks.py         # Celery tasks
│   └── requirements.txt # Dependencies
│
├── Frontend/            # Vue.js UI
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md            # Full documentation
```

## 🐛 Troubleshooting

### CORS Errors
```
Error: Access to XMLHttpRequest blocked by CORS
```
**Solution**: Ensure Flask backend is running on `http://localhost:5000` and check CORS config in `app.py`.

### Database Locked
```
Error: database is locked
```
**Solution**:
```bash
cd Backend
rm hms2026.db  # Delete database
python init_db.py  # Reinitialize
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Redis Connection Error
```
Error: Error connecting to redis
```
**Solution**: 
- Check if Redis is running: `redis-cli ping` (should return "PONG")
- Start Redis if not running
- Check Redis URL in `.env` file

### JWT Token Expired
```
401 Unauthorized
```
**Solution**: Refresh browser or clear localStorage and login again

## 🔧 Environment Configuration

Create a `.env` file in the `Backend/` directory:

```env
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key-here

# Redis (for Celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (optional for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password
```

## 📝 Development Workflow

1. **Backend changes**: Restart Flask server (`python app.py`)
2. **Frontend changes**: Auto-refreshes with Vite (just save file)
3. **Database changes**: Delete `hms2026.db` and reinit with `python init_db.py`
4. **New dependencies**: 
   - Backend: `pip install package` then update `requirements.txt`
   - Frontend: `npm install package` (auto-updates package.json)

## 🚀 Production Deployment

Before deploying:
1. Change `JWT_SECRET_KEY` in `.env`
2. Set `FLASK_ENV=production`
3. Enable SSL/HTTPS
4. Configure email service properly
5. Use a production database (PostgreSQL)
6. Set up proper Celery broker/backend (Redis cluster)
7. Use Gunicorn/uWSGI for Flask
8. Enable caching headers

See [README.md](README.md) for more details.

## 📞 Need Help?

- Check terminal output for specific error messages
- Verify all services are running (Flask, Redis, optional: Celery)
- Ensure correct Python version: `python --version` (need 3.8+)
- Check Node version: `node --version` (need 14+)

---

**Happy coding! 🚀**
