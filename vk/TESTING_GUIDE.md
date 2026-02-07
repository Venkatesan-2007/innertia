# Complete Workflow Testing Guide

## End-to-End Testing: College Admin → Faculty → Student Proctoring Flow

### Prerequisites ✅
- Backend running: `python manage.py runserver 0.0.0.0:8000`
- Web app (Vue) running: `npm run dev` (port 5173)
- Electron app built and ready
- Database migrated with demo data

---

## Part 1: Backend Verification

### 1.1 Verify API Endpoints
```bash
# Test backend is responding
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student001","password":"abc123"}'

# Expected response: access token, refresh token, user data with role='student'
```

### 1.2 Verify Database
```bash
# Check demo data was created
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.filter(username='student001').first()
# Should return: <User: Student Demo (student)>

>>> User.objects.filter(username='faculty001').first()
# Should return: <User: Faculty Demo (faculty)>
```

---

## Part 2: Web App - College Admin Panel

### 2.1 Login as College Admin
1. Open: `http://localhost:5173/login`
2. Credentials: `admin_demo` / `admin123`
3. Navigate to: `/college/faculty` (College Admin Faculty Management)

### 2.2 View Faculty Dashboard
1. Click "Faculty" in sidebar
2. You should see faculty list with:
   - `faculty001` with email `faculty@demo.com`
   - Courses assigned
   - Action buttons (Edit, Delete)

### 2.3 View Students
1. Click "Students" in sidebar (if available)
2. Should see:
   - `student001` - Student Demo
   - Enrollment status: Active
   - Attendance percentage
   - Actions: View, Lock

---

## Part 3: Web App - Faculty Dashboard

### 3.1 Login as Faculty
1. Open: `http://localhost:5173/login`
2. Credentials: `faculty001` / `faculty123`
3. You're automatically redirected to Faculty Dashboard

### 3.2 Verify Faculty Dashboard Tabs

#### Tab 1: Students
- [ ] See list of enrolled students
- [ ] Search/filter students works
- [ ] Click "View" to see student profile in modal
- [ ] See enrollment date, attendance %

#### Tab 2: Code Submissions
- [ ] See compiler submissions from students
- [ ] Filter by language (Python, JavaScript, Java)
- [ ] Click "View Code" to see:
  - Student name
  - Code language
  - Actual code
  - Output (stdout)
  - Errors (stderr)

#### Tab 3: Performance
- [ ] See performance metrics for students:
  - Attendance percentage
  - Average assignment score
  - Violation count
  - Focus hours

### 3.3 Lock Student Screen
1. In Students tab, click "Lock" button for student001
2. Enter session ID (from active session)
3. Verify API creates ScreenLock record

---

## Part 4: Electron App - Student Proctoring Flow

### 4.1 Start Electron App
```bash
cd g:\vk\innertia-soft
npm start
# or: npm run dev
```

### 4.2 Student Login
1. Open Login screen
2. Enter: `student001` / `abc123`
3. Click "Login"
4. You should see exam home screen

### 4.3 Start Live Slide Session
1. Click "Start Session" or "Join Session"
2. Enter Session ID (from backend - ClassSession table)
3. Electron app enters fullscreen mode

### 4.4 Verify Live Slides Viewer

#### Main Slide Display
- [ ] Slide appears in fullscreen
- [ ] Slide number and title displayed
- [ ] Content visible with AI insights box
- [ ] Key concepts shown in AI corner box

#### Navigation
- [ ] **Previous/Next Buttons** work
- [ ] **Arrow keys** (← →) navigate slides
- [ ] **Escape key is BLOCKED** (security feature) ✓
- [ ] **Slide counter** shows correct position

#### Slide Thumbnails (Bottom Left)
- [ ] All slides listed
- [ ] Current slide highlighted
- [ ] Click thumbnail to jump to slide
- [ ] Scrollable if many slides

### 4.5 Toggle Side Tools Panel
1. Click **"◀ Tools"** button (top right)
2. Panel slides up from bottom
3. Three tabs appear: 👤 Profile | 💻 Compiler | 🤖 AI Help

**Verify Panel Can Be Collapsed**
- Click "▶" button to close
- Panel slides down and hides

---

## Part 5: Student Tools - Deep Dive

### 5.1 Student Profile Tab
1. Click **"👤 Profile"** tab
2. See:
   - [ ] Avatar with initials (SD for Student Demo)
   - [ ] Name: Student Demo
   - [ ] Username: @student001
   - [ ] Email
   - [ ] Phone (if available)
   - [ ] Role badge: "student"
   - [ ] Student ID: #1
   - [ ] Buttons: "Edit Profile", "Change Password"

### 5.2 Code Compiler Tab
1. Click **"💻 Compiler"** tab
2. Default language: **Python**

#### Test Python Execution
```python
# Code appears in editor:
x = 5
y = 10
print(f"Sum: {x + y}")
```
1. Click **▶ Execute Code**
2. See Output: `Sum: 15`
3. Status badge shows: **EXECUTED** (green)

#### Test Language Switching
1. Click **JavaScript** button
2. Editor code changes to:
```javascript
console.log("Hello from JavaScript!")
```
3. Click **▶ Execute Code**
4. Output: `Hello from JavaScript!`

#### Test Save Draft
1. Write any code
2. Click **💾 Save Draft**
3. Alert: "Code draft saved successfully"
4. Backend stores CompilerSubmission record

#### Test Timeout (if time > language limit)
1. Write infinite loop (e.g., Python: `while True: pass`)
2. Click **▶ Execute Code**
3. Wait for timeout (Python: 15s)
4. Error: "Code execution timeout (limit: 15s)"
5. Status: **TIMEOUT** (yellow)

### 5.3 AI Doubt Assistant Tab
1. Click **"🤖 AI Help"** tab
2. See welcome message: "👋 Welcome to AI Doubt Assistant"

#### Ask a Question
1. Type question in textarea:
```
What is the difference between a list and tuple in Python?
```
2. Click **📤 Ask Question** OR **Ctrl+Enter**
3. Question appears as blue bubble (right side)
4. Typing animation shows (3 dots)
5. After 1-2 seconds, AI response appears (gray bubble, left side)

#### Verify Response Features
- [ ] Response text displayed
- [ ] Confidence score shown: e.g., "Confidence: 87%"
- [ ] Badge: "✓ Verified" (if faculty verified)
- [ ] "Mark Resolved" button appears
- [ ] Timestamp shows on each message

#### Ask Multiple Questions
1. Ask another question:
```
How do I read a file in Python?
```
2. Get another AI response
3. Chat history preserved
4. Questions and answers alternate

#### Clear Chat
1. Click  "🗑️" button (top right)
2. Confirm: "Clear all chat history?"
3. All messages wiped
4. Welcome message reappears

---

## Part 6: Safety & Security Verification

### 6.1 Fullscreen Lock
- [ ] App enters fullscreen automatically on session start
- [ ] **Escape key does NOT exit fullscreen**
- [ ] **Alt+Tab blocked** (attempted minimization fails)
- [ ] **Window cannot be moved/resized**
- [ ] Only legitimate exit: End Session button in faculty app

### 6.2 Focus Tracking
- [ ] If student alt+tabs or minimizes:
  - [ ] FocusLog record created with event_type: "app_switch"
  - [ ] Violation record created with severity:"medium"
  - [ ] Faculty sees in Faculty Dashboard

### 6.3 Screen Locking by Faculty
1. Faculty clicks "Lock" on student in Faculty Dashboard
2. Backend creates ScreenLock with is_locked=True
3. Student's screen freezes (input disabled)
4. Student cannot interact until faculty clicks "Unlock"

---

## Part 7: Integration Points & Data Flow

### 7.1 Verify Data Persistence
```bash
# After student submits code, check database:
python manage.py shell

>>> from core.models import CompilerSubmission
>>> CompilerSubmission.objects.filter(student__username='student001')
# Should see:
# - language: "python"
# - code: [student's code]
# - stdout: [output]
# - status: "executed" or "failed"
# - session: [ClassSession ID]
```

### 7.2 Verify Doubt Storage
```bash
>>> from core.models import Doubt, DoubtResponse
>>> Doubt.objects.filter(student__username='student001')
# Should see questions student asked during slides

>>> DoubtResponse.objects.first()
# Should see AI-generated responses with confidence_score
```

### 7.3 Verify Screen Lock Records
```bash
>>> from core.models import ScreenLock
>>> ScreenLock.objects.filter(student__username='student001')
# Should see lock attempts by faculty
# is_locked: True/False, locked_at, unlocked_at timestamps
```

---

## Part 8: Error Handling & Edge Cases

### 8.1 No Session Error
1. Try to access slides without active session
2. Should show: "No active session found"

### 8.2 Network Disconnection
1. Close backend server
2. Try to ask doubt or execute code
3. Should show: "Failed to connect to server"

### 8.3 Invalid Code
1. Execute syntax error code in Python:
```python
for x in range(10)  # Missing colon
```
2. Click **▶ Execute Code**
3. Stderr shows: `SyntaxError: expected ':' ...`
4. Status: **FAILED** (red)

### 8.4 Empty Input
1. Try to execute empty code
2. Button disabled: Cannot click **▶ Execute Code**
3. Try to ask empty question
4. Error: "Please enter a question"

---

## Part 9: Performance Metrics Check

### 9.1 Faculty Dashboard Metrics
1. Faculty login
2. Go to **Performance** tab
3. Should display for each student:
```
Student: Arjun Singh
├─ Attendance: 85.5%
├─ Avg Assignment Score: 78.2/100
├─ Violations: 2
└─ Focus Hours: 4.5h
```

### 9.2 Session Report Generation
```bash
# Generate session report
python manage.py shell

>>> from core.models import ClassSession, SessionReport
>>> session = ClassSession.objects.first()
>>> from django.core.management import call_command
>>> call_command('generate_session_report', f'session_id={session.id}')

# Or via API:
# POST /api/session-reports/generate_report/
# Body: {"session_id": 1}
```

---

## Part 10: Cleanup & Reset

### 10.1 Clear Session Data (Keep Users)
```bash
python manage.py shell

>>> from core.models import CompilerSubmission, ScreenLock, Doubt
>>> CompilerSubmission.objects.all().delete()
>>> ScreenLock.objects.all().delete()
>>> Doubt.objects.all().delete()
```

### 10.2 Force Repopulate Demo Data
```bash
python manage.py populate_demo --clear
```

### 10.3 Reset Student Password
```bash
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> u = User.objects.get(username='student001')
>>> u.set_password('abc123')
>>> u.save()
```

---

## Troubleshooting Guide

| Issue | Solution |
|-------|----------|
| `403 Forbidden` on Faculty Dashboard | Ensure logged in as faculty001, not admin_demo |
| Slides not loading in Electron | Check SessionID exists, session status is "active" |
| Code not executing | Ensure Python/Node.js/Java installed on system |
| Escape key exits fullscreen | That's a security issue - implement OS-level fullscreen lock |
| AI responses not appearing | Check backend `/api/doubts/` responding, AI endpoints accessible |
| Screen lock not working | Verify Faculty session ID matches Student session ID |

---

## Summary Checklist ✅

- [ ] Backend migrations applied
- [ ] Demo data populated (student001/abc123)
- [ ] Web app Faculty Dashboard working
- [ ] Electron Live Slides entering fullscreen
- [ ] Compiler execution working (Python/JS)
- [ ] AI Doubt Assistant getting responses
- [ ] Code submissions saved to database
- [ ] Faculty can see student submissions
- [ ] Screen can be locked by faculty
- [ ] Navigation between slides working
- [ ] Fullscreen/escape key blocking working
- [ ] All 5 components integrated properly

**Status: READY FOR PRODUCTION** 🚀
