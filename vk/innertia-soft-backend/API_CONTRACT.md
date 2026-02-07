# API Contract Documentation - Innertia Backend

**Base URL:** `http://localhost:8000/api/`  
**Auth Header:** `Authorization: Bearer <JWT_TOKEN>`

---

## 🔐 Authentication Endpoints

### 1. Login / Obtain JWT Token
```
POST /auth/token/
Content-Type: application/json

REQUEST:
{
  "username": "student_user",
  "password": "password123"
}

RESPONSE (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "student",
  "id": 1
}

ERROR (401):
{
  "detail": "Invalid credentials"
}
```

### 2. Refresh JWT Token
```
POST /auth/token/refresh/
Content-Type: application/json

REQUEST:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

RESPONSE (200):
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Register New User
```
POST /users/register/
Content-Type: application/json

REQUEST:
{
  "username": "new_student",
  "email": "student@university.edu",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student"
}

RESPONSE (201):
{
  "id": 5,
  "username": "new_student",
  "email": "student@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "college": null,
  "phone": "",
  "date_joined": "2024-02-07T10:30:00Z"
}

ERROR (400):
{
  "username": ["A user with that username already exists."],
  "password": ["Passwords don't match"]
}
```

### 4. Get Current User Profile
```
GET /users/me/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
{
  "id": 1,
  "username": "student_user",
  "email": "student@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "college": 1,
  "phone": "9876543210",
  "date_joined": "2024-01-15T08:00:00Z"
}

ERROR (401):
{
  "detail": "Authentication required"
}
```

---

## 🏫 Institution Endpoints

### 5. Get All Colleges
```
GET /colleges/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "MIT Delhi",
      "code": "MITD",
      "address": "New Delhi, India",
      "city": "Delhi",
      "country": "India",
      "admin": 1,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 6. Get All Courses
```
GET /courses/?program=1&semester=4
Authorization: Bearer <JWT_TOKEN>

QUERY PARAMS:
- program (optional)
- faculty (optional)
- semester (optional)

RESPONSE (200):
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "code": "CS101",
      "name": "Data Structures",
      "description": "Learn DS...",
      "program": 1,
      "program_name": "Computer Science",
      "faculty": 2,
      "faculty_name": "Dr. Smith",
      "semester": 4,
      "credits": 3,
      "created_at": "2024-01-10T00:00:00Z"
    }
  ]
}
```

### 7. Enroll Student in Course
```
POST /courses/1/enroll_student/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student_id": 5
}

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "course": 1,
  "course_code": "CS101",
  "enrolled_date": "2024-02-07T10:00:00Z",
  "status": "active"
}

ERROR (400):
{
  "detail": "student_id is required"
}
```

### 8. Get Enrolled Students in Course
```
GET /courses/1/enrolled_students/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
[
  {
    "id": 1,
    "student": 5,
    "student_name": "John Doe",
    "course": 1,
    "course_code": "CS101",
    "enrolled_date": "2024-02-07T10:00:00Z",
    "status": "active"
  }
]
```

---

## 📚 Class Session & Attendance

### 9. Create Class Session
```
POST /sessions/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "course": 1,
  "faculty": 2,
  "session_date": "2024-02-07T10:00:00Z",
  "duration_minutes": 60,
  "topic": "Arrays and Lists",
  "status": "scheduled",
  "session_notes": "First class on arrays"
}

RESPONSE (201):
{
  "id": 1,
  "course": 1,
  "course_code": "CS101",
  "faculty": 2,
  "faculty_name": "Dr. Smith",
  "session_date": "2024-02-07T10:00:00Z",
  "duration_minutes": 60,
  "topic": "Arrays and Lists",
  "status": "scheduled",
  "notes": "First class on arrays",
  "created_at": "2024-02-07T09:00:00Z",
  "updated_at": "2024-02-07T09:00:00Z"
}
```

### 10. Start Class Session
```
POST /sessions/1/start_session/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
{
  "id": 1,
  "...": "...",
  "status": "active"
}
```

### 11. End Class Session
```
POST /sessions/1/end_session/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
{
  "id": 1,
  "...": "...",
  "status": "completed"
}
```

### 12. Get Attendance Report for Session
```
GET /sessions/1/attendance_report/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
[
  {
    "id": 1,
    "student": 5,
    "student_name": "John Doe",
    "session": 1,
    "session_topic": "Arrays and Lists",
    "status": "present",
    "active_minutes": 58,
    "total_minutes": 60,
    "attendance_percentage": 96.67,
    "check_in_time": "2024-02-07T10:02:00Z",
    "check_out_time": "2024-02-07T11:00:00Z",
    "recorded_at": "2024-02-07T10:02:00Z"
  }
]
```

### 13. Mark/Update Attendance
```
POST /attendance/mark_attendance/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student_id": 5,
  "session_id": 1,
  "status": "present",
  "active_minutes": 58
}

RESPONSE (200):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "session": 1,
  "session_topic": "Arrays and Lists",
  "status": "present",
  "active_minutes": 58,
  "total_minutes": 60,
  "attendance_percentage": 96.67,
  "check_in_time": "2024-02-07T10:02:00Z",
  "check_out_time": null,
  "recorded_at": "2024-02-07T10:02:00Z"
}

AUTO-STATUS RULES:
- active_minutes >= 80% of total_minutes → "present"
- 50-79% → "late"
- < 50% → "absent"
```

---

## 🎬 Focus & Violations

### 14. Log Focus Event
```
POST /focus-logs/log_event/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student": 5,
  "session": 1,
  "event_type": "fullscreen_exit",
  "metadata": {
    "timestamp": "2024-02-07T10:30:00Z",
    "additional_info": "Student clicked out of fullscreen"
  }
}

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "session": 1,
  "event_type": "fullscreen_exit",
  "timestamp": "2024-02-07T10:30:00Z",
  "metadata": {
    "timestamp": "2024-02-07T10:30:00Z",
    "additional_info": "..."
  }
}

VALID EVENT TYPES:
- focus_gained
- focus_lost
- fullscreen_exit
- alt_tab
- app_switch
- minimized
```

### 15. Create Violation Record
```
POST /violations/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student": 5,
  "session": 1,
  "violation_type": "fullscreen_exit",
  "severity": "high",
  "description": "Exited fullscreen mode during exam."
}

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "session": 1,
  "violation_type": "fullscreen_exit",
  "severity": "high",
  "description": "Exited fullscreen mode during exam.",
  "timestamp": "2024-02-07T10:30:00Z",
  "is_resolved": false,
  "resolution_notes": ""
}

SEVERITY LEVELS:
- low
- medium (default)
- high
- critical
```

### 16. Resolve Violation
```
POST /violations/1/resolve_violation/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "resolution_notes": "Student was given a warning."
}

RESPONSE (200):
{
  "id": 1,
  "...": "...",
  "is_resolved": true,
  "resolution_notes": "Student was given a warning."
}
```

---

## 📝 Content & Materials

### 17. Add Slide to Session
```
POST /slides/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "session": 1,
  "slide_number": 1,
  "title": "Introduction to Data Structures",
  "content": "Arrays are the most basic data structure...",
  "image_url": "https://example.com/slide1.png",
  "ai_summary": "Comprehensive overview of arrays and their properties.",
  "ai_definitions": ["Array", "Index", "Element", "Dimension"],
  "ai_questions": [
    "What is an array?",
    "What are the advantages of arrays?"
  ]
}

RESPONSE (201):
{
  "id": 1,
  "session": 1,
  "slide_number": 1,
  "title": "Introduction to Data Structures",
  "content": "Arrays are the most basic...",
  "image_url": "https://example.com/slide1.png",
  "ai_summary": "Comprehensive overview...",
  "ai_definitions": ["Array", "Index", "Element", "Dimension"],
  "ai_questions": ["What is an array?", "..."],
  "created_at": "2024-02-07T10:00:00Z"
}
```

### 18. Create Student Note
```
POST /notes/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student": 5,
  "session": 1,
  "slide": 1,
  "title": "Arrays - My Notes",
  "content": "# Arrays\n\n- Fixed size collection\n- Index-based access\n- O(1) access time",
  "tags": ["arrays", "data-structures", "important"],
  "is_public": false
}

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "session": 1,
  "slide": 1,
  "title": "Arrays - My Notes",
  "content": "# Arrays\n\n-...",
  "tags": ["arrays", "data-structures", "important"],
  "is_public": false,
  "created_at": "2024-02-07T10:30:00Z",
  "updated_at": "2024-02-07T10:30:00Z"
}
```

---

## 🤖 Doubts & AI Responses

### 19. Ask a Doubt
```
POST /doubts/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "student": 5,
  "session": 1,
  "question": "What is the time complexity of array access?",
  "status": "open"
}

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "session": 1,
  "question": "What is the time complexity of array access?",
  "status": "open",
  "asked_at": "2024-02-07T10:35:00Z",
  "resolved_at": null,
  "response": null
}
```

### 20. Get AI Response for Doubt
```
GET /doubt-responses/?doubt=1
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
[
  {
    "id": 1,
    "doubt": 1,
    "answer": "The time complexity of array access is O(1) because arrays are contiguous in memory and support index-based access.",
    "source_slide": 1,
    "slide_title": "Introduction to Data Structures",
    "source_snippet": "Arrays provide constant-time access to elements via indexing.",
    "confidence_score": 0.95,
    "generated_by_ai": true,
    "faculty_verified": true,
    "responded_at": "2024-02-07T10:36:00Z"
  }
]
```

### 21. Resolve Doubt
```
POST /doubts/1/resolve_doubt/
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "session": 1,
  "question": "...",
  "status": "resolved",
  "asked_at": "2024-02-07T10:35:00Z",
  "resolved_at": "2024-02-07T10:37:00Z",
  "response": {...}
}
```

---

## 📋 Assignments & Submissions

### 22. Create Assignment
```
POST /assignments/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "course": 1,
  "title": "Implement a Stack using Arrays",
  "description": "Create an implementation...",
  "due_date": "2024-02-14T23:59:00Z",
  "status": "published",
  "max_score": 100.0
}

RESPONSE (201):
{
  "id": 1,
  "course": 1,
  "course_code": "CS101",
  "title": "Implement a Stack using Arrays",
  "description": "Create an implementation...",
  "due_date": "2024-02-14T23:59:00Z",
  "status": "published",
  "max_score": 100.0,
  "created_at": "2024-02-07T11:00:00Z"
}
```

### 23. Submit Assignment
```
POST /submissions/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
OR multipart/form-data for file upload

REQUEST (JSON):
{
  "student": 5,
  "assignment": 1,
  "content": "class Stack:\n    def __init__(self):\n        self.items = []",
  "file": null,
  "status": "submitted"
}

REQUEST (with file):
multipart/form-data
- student: 5
- assignment: 1
- content: "Optional text content"
- file: <binary file>
- status: "submitted"

RESPONSE (201):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "assignment": 1,
  "assignment_title": "Implement a Stack using Arrays",
  "content": "class Stack:...",
  "file": null,
  "status": "submitted",
  "score": null,
  "feedback": "",
  "submitted_at": "2024-02-10T15:30:00Z",
  "graded_at": null
}
```

### 24. Grade Submission
```
POST /submissions/1/grade_submission/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "score": 85.5,
  "feedback": "Good implementation, but could optimize space further."
}

RESPONSE (200):
{
  "id": 1,
  "student": 5,
  "student_name": "John Doe",
  "assignment": 1,
  "assignment_title": "...",
  "content": "...",
  "file": null,
  "status": "graded",
  "score": 85.5,
  "feedback": "Good implementation...",
  "submitted_at": "2024-02-10T15:30:00Z",
  "graded_at": "2024-02-11T09:00:00Z"
}
```

---

## 📊 Analytics & Reports

### 25. Generate Session Report
```
POST /session-reports/generate_report/
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

REQUEST:
{
  "session_id": 1
}

RESPONSE (200):
{
  "id": 1,
  "session": 1,
  "session_info": {...class session details...},
  "total_students": 40,
  "present_count": 38,
  "absent_count": 2,
  "average_attendance_percentage": 94.5,
  "violation_count": 3,
  "focus_duration_minutes": 2280,
  "generated_at": "2024-02-07T12:00:00Z"
}
```

### 26. Get Student Performance
```
GET /student-performance/?student=5&course=1
Authorization: Bearer <JWT_TOKEN>

RESPONSE (200):
[
  {
    "id": 1,
    "student": 5,
    "student_name": "John Doe",
    "course": 1,
    "course_code": "CS101",
    "total_attendance_percentage": 94.5,
    "average_assignment_score": 87.3,
    "violation_count": 1,
    "total_focus_hours": 38.5,
    "last_updated": "2024-02-07T12:00:00Z"
  }
]
```

---

## Error Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Duplicate record |
| 500 | Server Error - Internal error |

---

## 📌 Important Notes

1. **All timestamps** are in UTC ISO format: `YYYY-MM-DDTHH:MM:SSZ`
2. **Pagination:** List endpoints return paginated results with `count`, `next`, `previous`, `results`
3. **Filtering:** Use query params like `?field=value`
4. **Ordering:** Use `-` prefix for descending order: `?ordering=-created_at`
5. **JWT Token:** Expires in 1 hour, use refresh token to get new access token
6. **Refresh Token:** Expires in 7 days

---

**Last Updated:** February 7, 2026
