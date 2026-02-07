from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import (
    College, Program, Course, Enrollment, ClassSession, Attendance,
    Violation, FocusLog, Slide, Note, Doubt, Assignment, Submission, StudentPerformance
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with demo data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            # Careful with this!
            # ClassSession.objects.all().delete()
            # College.objects.all().delete()
            # User.objects.filter(role__in=['faculty', 'student']).delete()

        self.stdout.write(self.style.SUCCESS('Starting demo data population...'))

        # Create Colleges
        self.stdout.write('  > Creating colleges...')
        college1, _ = College.objects.get_or_create(
            code='IIT001',
            defaults={
                'name': 'Indian Institute of Technology - Delhi',
                'address': '123 Education Street, New Delhi',
                'city': 'New Delhi',
                'country': 'India'
            }
        )

        college2, _ = College.objects.get_or_create(
            code='DU001',
            defaults={
                'name': 'Delhi University - Main Campus',
                'address': '456 Academic Lane, New Delhi',
                'city': 'New Delhi',
                'country': 'India'
            }
        )

        # Create Programs
        self.stdout.write('  > Creating programs...')
        prog_cs, _ = Program.objects.get_or_create(
            code='CS101',
            college=college1,
            defaults={
                'name': 'Computer Science (B.Tech)',
                'duration_semesters': 8
            }
        )

        prog_ee, _ = Program.objects.get_or_create(
            code='EE101',
            college=college1,
            defaults={
                'name': 'Electrical Engineering (B.Tech)',
                'duration_semesters': 8
            }
        )

        # Create Faculty Users
        self.stdout.write('  > Creating faculty users...')
        faculty1, _ = User.objects.get_or_create(
            username='dr.sharma',
            defaults={
                'email': 'dr.sharma@innertia.com',
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'role': 'faculty',
                'college': college1,
                'is_staff': False
            }
        )
        if faculty1.password == '':
            faculty1.set_password('faculty123')
            faculty1.save()

        faculty2, _ = User.objects.get_or_create(
            username='prof.gupta',
            defaults={
                'email': 'prof.gupta@innertia.com',
                'first_name': 'Priya',
                'last_name': 'Gupta',
                'role': 'faculty',
                'college': college1,
                'is_staff': False
            }
        )
        if faculty2.password == '':
            faculty2.set_password('faculty123')
            faculty2.save()

        # Create Courses
        self.stdout.write('  > Creating courses...')
        course1, _ = Course.objects.get_or_create(
            code='CS101',
            defaults={
                'name': 'Introduction to Programming',
                'description': 'Learn the basics of programming with Python',
                'program': prog_cs,
                'faculty': faculty1,
                'semester': 1,
                'credits': 4
            }
        )

        course2, _ = Course.objects.get_or_create(
            code='CS102',
            defaults={
                'name': 'Data Structures',
                'description': 'Master fundamental data structures and algorithms',
                'program': prog_cs,
                'faculty': faculty2,
                'semester': 2,
                'credits': 4
            }
        )

        # Create Student Users
        self.stdout.write('  > Creating student users...')
        student_names = [
            ('student001', 'Arjun', 'Singh', 'arjun@student.com'),
            ('student002', 'Priya', 'Nair', 'priya@student.com'),
            ('student003', 'Rohan', 'Patel', 'rohan@student.com'),
            ('student004', 'Ananya', 'Verma', 'ananya@student.com'),
            ('student005', 'Vihaan', 'Reddy', 'vihaan@student.com'),
        ]

        students = []
        for username, first_name, last_name, email in student_names:
            student, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'student',
                    'college': college1,
                    'is_staff': False
                }
            )
            if student.password == '':
                # Use "abc123" for student001, "student123" for others
                password = 'abc123' if username == 'student001' else 'student123'
                student.set_password(password)
                student.save()
            students.append(student)

        # Create Enrollments
        self.stdout.write('  > Creating enrollments...')
        for student in students:
            for course in [course1, course2]:
                Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={'status': 'active'}
                )

        # Create Class Sessions
        self.stdout.write('  > Creating class sessions...')
        now = timezone.now()

        session1 = ClassSession.objects.create(
            course=course1,
            faculty=faculty1,
            session_date=now,
            duration_minutes=60,
            topic='Introduction to Python',
            session_notes='Getting started with Python fundamentals',
            status='completed'
        )

        session2 = ClassSession.objects.create(
            course=course2,
            faculty=faculty2,
            session_date=now - timedelta(days=1),
            duration_minutes=60,
            topic='Arrays and Lists',
            session_notes='Understanding array and list data structures',
            status='completed'
        )

        # Create Attendance Records
        self.stdout.write('  > Creating attendance records...')
        for student in students:
            Attendance.objects.get_or_create(
                student=student,
                session=session1,
                defaults={
                    'status': 'present',
                    'active_minutes': 55,
                    'attendance_percentage': 92.0,
                    'check_in_time': now,
                    'check_out_time': now + timedelta(hours=1)
                }
            )

        # Create Assignments
        self.stdout.write('  > Creating assignments...')
        assignment1 = Assignment.objects.create(
            course=course1,
            title='Python Basics Challenge',
            description='Write Python programs for basic programming concepts',
            due_date=now + timedelta(days=7),
            status='published',
            max_score=100.0
        )

        # Create Submissions
        self.stdout.write('  > Creating submissions...')
        for idx, student in enumerate(students):
            Submission.objects.get_or_create(
                student=student,
                assignment=assignment1,
                defaults={
                    'content': f'# Solution by {student.first_name}\nprint("Hello, World!")',
                    'status': 'submitted' if idx < 3 else 'draft',
                    'submitted_at': now - timedelta(days=1) if idx < 3 else None
                }
            )

        # Create Focus Logs
        self.stdout.write('  > Creating focus logs...')
        for student in students[:2]:
            for i in range(5):
                FocusLog.objects.get_or_create(
                    student=student,
                    session=session1,
                    timestamp=now - timedelta(minutes=(5-i)*10),
                    defaults={
                        'event_type': 'focus_shift' if i % 2 == 0 else 'tab_switch',
                        'metadata': {'attempt': i+1}
                    }
                )

        # Create Violations
        self.stdout.write('  > Creating violations...')
        Violation.objects.get_or_create(
            student=students[0],
            session=session1,
            defaults={
                'violation_type': 'test_window_blur',
                'severity': 'medium',
                'description': 'Student switched away from exam window twice',
                'timestamp': now,
                'is_resolved': False
            }
        )

        # Create Student Performance Records
        self.stdout.write('  > Creating performance records...')
        for student in students[:3]:
            StudentPerformance.objects.get_or_create(
                student=student,
                course=course1,
                defaults={
                    'total_attendance_percentage': 85.0,
                    'average_assignment_score': 78.0,
                    'violation_count': 1,
                    'total_focus_hours': 12.5
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Demo data population complete!'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Demo Credentials:'))
        self.stdout.write('  Faculty: dr.sharma / faculty123')
        self.stdout.write('  Student: student001 / student123')
        self.stdout.write(self.style.SUCCESS('Admin user: admin / admin123'))
