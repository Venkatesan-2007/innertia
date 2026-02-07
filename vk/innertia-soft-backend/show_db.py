import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innertia.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import *

print("=" * 80)
print("INNERTIA DATABASE CONTENTS")
print("=" * 80)

User = get_user_model()

print("\n[USERS]")
print("-" * 80)
for user in User.objects.all():
    print(f"ID: {user.id} | Username: {user.username} | Email: {user.email} | Role: {user.role}")
    print(f"  Name: {user.first_name} {user.last_name} | Staff: {user.is_staff} | Active: {user.is_active}")
    print()

print("[COLLEGES]")
print("-" * 80)
colleges = College.objects.all()
print(f"Total: {colleges.count()}")
for college in colleges:
    print(f"ID: {college.id} | Name: {college.name} | Code: {college.code} | City: {college.city}")
print()

print("[PROGRAMS]")
print("-" * 80)
programs = Program.objects.all()
print(f"Total: {programs.count()}")
for program in programs:
    print(f"ID: {program.id} | Name: {program.name} | Code: {program.code} | College: {program.college}")
print()

print("[COURSES]")
print("-" * 80)
courses = Course.objects.all()
print(f"Total: {courses.count()}")
for course in courses:
    print(f"ID: {course.id} | Code: {course.code} | Name: {course.name} | Faculty: {course.faculty}")
print()

print("[CLASS SESSIONS]")
print("-" * 80)
sessions = ClassSession.objects.all()
print(f"Total: {sessions.count()}")
for session in sessions:
    print(f"ID: {session.id} | Course: {session.course} | Topic: {session.topic} | Date: {session.session_date}")
print()

print("[ENROLLMENTS]")
print("-" * 80)
enrollments = Enrollment.objects.all()
print(f"Total: {enrollments.count()}")
for enroll in enrollments:
    print(f"ID: {enroll.id} | Student: {enroll.student} | Course: {enroll.course} | Status: {enroll.status}")
print()

print("[ATTENDANCE]")
print("-" * 80)
attendance = Attendance.objects.all()
print(f"Total: {attendance.count()}")
for att in attendance:
    print(f"ID: {att.id} | Student: {att.student} | Session: {att.session} | Status: {att.status}")
print()

print("[VIOLATIONS]")
print("-" * 80)
violations = Violation.objects.all()
print(f"Total: {violations.count()}")
for v in violations:
    print(f"ID: {v.id} | Student: {v.student} | Type: {v.violation_type} | Severity: {v.severity}")
print()

print("[FOCUS LOGS]")
print("-" * 80)
focus_logs = FocusLog.objects.all()
print(f"Total: {focus_logs.count()}")
for log in focus_logs:
    print(f"ID: {log.id} | Student: {log.student} | Event: {log.event_type} | Time: {log.timestamp}")
print()

print("[SLIDES]")
print("-" * 80)
slides = Slide.objects.all()
print(f"Total: {slides.count()}")
for slide in slides:
    print(f"ID: {slide.id} | Session: {slide.session} | Slide #{slide.slide_number} | Title: {slide.title}")
print()

print("[NOTES]")
print("-" * 80)
notes = Note.objects.all()
print(f"Total: {notes.count()}")
for note in notes:
    print(f"ID: {note.id} | Student: {note.student} | Title: {note.title} | Public: {note.is_public}")
print()

print("[DOUBTS]")
print("-" * 80)
doubts = Doubt.objects.all()
print(f"Total: {doubts.count()}")
for doubt in doubts:
    question_preview = doubt.question[:50] if len(doubt.question) > 50 else doubt.question
    print(f"ID: {doubt.id} | Student: {doubt.student} | Q: {question_preview}... | Status: {doubt.status}")
print()

print("[ASSIGNMENTS]")
print("-" * 80)
assignments = Assignment.objects.all()
print(f"Total: {assignments.count()}")
for assign in assignments:
    print(f"ID: {assign.id} | Course: {assign.course} | Title: {assign.title} | Status: {assign.status}")
print()

print("[SUBMISSIONS]")
print("-" * 80)
submissions = Submission.objects.all()
print(f"Total: {submissions.count()}")
for sub in submissions:
    print(f"ID: {sub.id} | Student: {sub.student} | Assignment: {sub.assignment} | Status: {sub.status}")
print()

print("[SESSION REPORTS]")
print("-" * 80)
reports = SessionReport.objects.all()
print(f"Total: {reports.count()}")
for report in reports:
    print(f"ID: {report.id} | Session: {report.session} | Present: {report.present_count} | Absent: {report.absent_count}")
print()

print("[STUDENT PERFORMANCE]")
print("-" * 80)
perf = StudentPerformance.objects.all()
print(f"Total: {perf.count()}")
for p in perf:
    print(f"ID: {p.id} | Student: {p.student} | Course: {p.course} | Attendance: {p.total_attendance_percentage}%")
print()

print("=" * 80)
print("DATABASE SUMMARY")
print("=" * 80)
print(f"Total Users: {User.objects.count()}")
print(f"Total Colleges: {College.objects.count()}")
print(f"Total Programs: {Program.objects.count()}")
print(f"Total Courses: {Course.objects.count()}")
print(f"Total Enrollments: {Enrollment.objects.count()}")
print(f"Total Sessions: {ClassSession.objects.count()}")
print(f"Total Attendance Records: {Attendance.objects.count()}")
print(f"Total Violations: {Violation.objects.count()}")
print(f"Total Focus Logs: {FocusLog.objects.count()}")
print(f"Total Slides: {Slide.objects.count()}")
print(f"Total Notes: {Note.objects.count()}")
print(f"Total Doubts: {Doubt.objects.count()}")
print(f"Total Assignments: {Assignment.objects.count()}")
print(f"Total Submissions: {Submission.objects.count()}")
print(f"Total Session Reports: {SessionReport.objects.count()}")
print(f"Total Student Performance Records: {perf.count()}")
print("=" * 80)
