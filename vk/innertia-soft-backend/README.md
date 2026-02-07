# Innertia Backend - Django REST API

Complete backend implementation for the Innertia education platform with secure exam mode, attendance tracking, AI-powered doubt clearing, and comprehensive analytics.

## 🏗️ Project Structure

```
innertia-soft-backend/
├── innertia/              # Project settings & configuration
│   ├── settings.py       # Django settings (PostgreSQL, JWT, CORS)
│   ├── urls.py           # Main URL router
│   └── wsgi.py           # WSGI application
├── core/                 # Main app with all models & API
│   ├── models.py         # Database models (15+ models)
│   ├── views.py          # API ViewSets & endpoints
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # API routes
│   ├── admin.py          # Django admin configuration
│   └── migrations/       # Database migrations
├── manage.py             # Django CLI
├── requirements.txt      # Python dependencies
└── .env.example         # Environment variables template
```

## 📦 Core Models (Locked Schema)

### Authentication & Users
- **User** - Custom user with roles (admin, faculty, student)
- **College** - Institution entity
- **Program** - Degree programs (e.g., Computer Science)

### Courses & Enrollment
- **Course** - Course definition with faculty assignment
- **Enrollment** - Student enrollment tracking

### Sessions & Attendance
- **ClassSession** - Scheduled class sessions
- **Attendance** - Student attendance records with focus tracking
- **FocusLog** - Raw focus events (blur, minimize, alt-tab)
- **Violation** - Security violations with severity levels

### Content & Materials
- **Slide** - PPT/PDF slides with AI-generated summaries
- **Note** - Student markdown notes linked to slides

### AI & Doubts
- **Doubt** - Student questions/doubts
- **DoubtResponse** - AI-generated or faculty answers with source tracking

### Assessments
- **Assignment** - Course assignments/tasks
- **Submission** - Student submissions with grading

### Analytics
- **SessionReport** - Aggregated session statistics
- **StudentPerformance** - Per-student, per-course performance metrics

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip/virtualenv

### 2. Setup Environment

```bash
# Clone the repo (if needed)
cd g:\vk\innertia-soft-backend

# Create and activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

#### Option A: PostgreSQL (Recommended for production)

**Windows:**
```powershell
# Install PostgreSQL if not already installed
# Create database and user:

psql -U postgres
CREATE DATABASE innertia_db;
CREATE USER innertia_user WITH PASSWORD 'secure_password';
ALTER ROLE innertia_user SET client_encoding TO 'utf8';
ALTER ROLE innertia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE innertia_user SET default_transaction_deferrable TO on;
ALTER ROLE innertia_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE innertia_db TO innertia_user;
\q
```

**macOS/Linux:**
```bash
sudo -u postgres psql
CREATE DATABASE innertia_db;
CREATE USER innertia_user WITH PASSWORD 'secure_password';
ALTER ROLE innertia_user SET client_encoding TO 'utf8';
ALTER ROLE innertia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE innertia_user SET default_transaction_deferrable TO on;
ALTER ROLE innertia_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE innertia_db TO innertia_user;
\q
```

### 4. Environment Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DEBUG=True
DB_NAME=innertia_db
DB_USER=innertia_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Enter username, email, password
```

### 7. Start Development Server

```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

API documentation available at:
- Django Admin: `http://localhost:8000/admin/`
- API Root: `http://localhost:8000/api/`

## 🔐 Authentication

### JWT Tokens

**Obtain Token:**
```bash
POST /api/auth/token/
{
  "username": "student_username",
  "password": "password"
}

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "student",
  "id": 1
}
```

**Use Token:**
```bash
Authorization: Bearer <access_token>
```

**Refresh Token:**
```bash
POST /api/auth/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📋 API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/users/register/` - Register new user
- `GET /api/users/me/` - Get current user profile

### Courses & Enrollment
- `GET/POST /api/courses/` - List/create courses
- `GET /api/courses/{id}/enrolled_students/` - List enrolled students
- `POST /api/courses/{id}/enroll_student/` - Enroll student
- `GET/POST /api/enrollments/` - Manage enrollments

### Sessions & Attendance
- `GET/POST /api/sessions/` - Manage class sessions
- `POST /api/sessions/{id}/start_session/` - Start session
- `POST /api/sessions/{id}/end_session/` - End session
- `GET /api/sessions/{id}/attendance_report/` - Get attendance report
- `GET/POST /api/attendance/` - Manage attendance
- `POST /api/attendance/mark_attendance/` - Mark/update attendance

### Focus & Violations
- `GET/POST /api/focus-logs/` - Log focus events
- `POST /api/focus-logs/log_event/` - Create focus log
- `GET/POST /api/violations/` - Manage violations
- `POST /api/violations/{id}/resolve_violation/` - Resolve violation

### Content
- `GET/POST /api/slides/` - Manage slides
- `GET/POST /api/notes/` - Manage notes

### AI & Doubts
- `GET/POST /api/doubts/` - Manage doubts
- `POST /api/doubts/{id}/ask_doubt/` - Ask new doubt
- `POST /api/doubts/{id}/resolve_doubt/` - Resolve doubt
- `GET/POST /api/doubt-responses/` - Manage responses

### Assessments
- `GET/POST /api/assignments/` - Manage assignments
- `GET/POST /api/submissions/` - Manage submissions
- `POST /api/submissions/{id}/grade_submission/` - Grade submission

### Analytics
- `GET /api/session-reports/` - Get session reports
- `POST /api/session-reports/generate_report/` - Generate report
- `GET /api/student-performance/` - Get performance data

## 🔄 Key Features

### Session Management
- **Status Flow:** scheduled → active → completed/cancelled
- **Real-time Tracking:** Focus logs, violations, attendance
- **Automatic Calculation:** Attendance % = (active_minutes / total_minutes)

### Attendance Logic
- **80%+ attendance** → Present ✅
- **50-79% attendance** → Late ⚠️
- **<50% attendance** → Absent ❌

### Focus Tracking Events
- `focus_gained` - Terminal gains focus
- `focus_lost` - Terminal loses focus
- `fullscreen_exit` - Fullscreen mode exited
- `alt_tab` - Alt+Tab detected
- `app_switch` - Application switched
- `minimized` - Window minimized

### Violation Severity
- **Low** - Minor infractions
- **Medium** - Standard violations (default)
- **High** - Serious violations
- **Critical** - Immediate action required

## 📊 Data Models Relationships

```
College (1) ──┬─→ (Many) Program
              ├─→ (Many) User (admin)
              
Program ──→ (Many) Course

Course (1) ──┬─→ (Many) ClassSession
             ├─→ (Many) Enrollment
             ├─→ (Many) Assignment
             └─→ (Many) StudentPerformance
             
User (1) ──┬─→ (Many) Enrollment (student role)
           ├─→ (Many) AttendanceRecords
           ├─→ (Many) FocusLogs
           ├─→ (Many) Violations
           ├─→ (Many) Notes
           ├─→ (Many) Doubts
           ├─→ (Many) Submissions
           └─→ (1) StudentPerformance

ClassSession (1) ──┬─→ (Many) Attendance
                   ├─→ (Many) FocusLog
                   ├─→ (Many) Violation
                   ├─→ (Many) Slide
                   └─→ (1) SessionReport

Doubt (1) ──→ (1) DoubtResponse
```

## 🛠️ Common Tasks

### Add Slides to Session
```python
POST /api/slides/
{
  "session": 1,
  "slide_number": 1,
  "title": "Introduction",
  "content": "Slide content...",
  "ai_summary": "Auto-generated summary",
  "ai_definitions": ["term1", "term2"],
  "ai_questions": ["Expected question 1"]
}
```

### Log Focus Event
```python
POST /api/focus-logs/log_event/
{
  "student": 1,
  "session": 1,
  "event_type": "fullscreen_exit",
  "metadata": {"timestamp": "2024-02-07T10:30:00Z"}
}
```

### Create Violation Record
```python
POST /api/violations/
{
  "student": 1,
  "session": 1,
  "violation_type": "fullscreen_exit",
  "severity": "high",
  "description": "Student exited fullscreen mode during exam"
}
```

### Ask a Doubt
```python
POST /api/doubts/
{
  "student": 1,
  "session": 1,
  "question": "What is Object-Oriented Programming?",
  "status": "open"
}
```

## 📈 Performance Optimization

- **Database Indexes** on frequently queried fields
- **Pagination** (20 items per page)
- **Filtering & Ordering** support on all list endpoints
- **Read-only Views** for analytics endpoints

## 🔒 Security Notes

- ✅ JWT authentication on all endpoints (except registration)
- ✅ Role-based access (admin, faculty, student)
- ✅ CORS configured for trusted domains
- ⚠️ Use environment variables for sensitive data
- ⚠️ Never commit `.env` file

## 🐛 Troubleshooting

### Database Connection Error
```
FATAL: password authentication failed
```
→ Check PostgreSQL credentials in `.env`

### Migration Errors
```
python manage.py migrate --fake-initial  # Use carefully
```

### Port Already in Use
```
python manage.py runserver 8001  # Use different port
```

## 📚 Technologies

- **Framework:** Django 4.2
- **API:** Django REST Framework 3.14
- **Authentication:** djangorestframework-simplejwt (JWT)
- **Database:** PostgreSQL 12+
- **CORS:** django-cors-headers

## 📖 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)

---

**Last Updated:** February 7, 2026  
**Version:** 1.0  
**Team:** Innertia Development
