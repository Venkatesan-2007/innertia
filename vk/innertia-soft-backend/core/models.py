from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# ======================
# User Roles & Auth
# ======================

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    college = models.ForeignKey('College', on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


# ======================
# Institution & Courses
# ======================

class College(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, 
                                 blank=True, related_name='college_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'colleges'
    
    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=255)  # e.g., "Computer Science"
    code = models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='programs')
    duration_semesters = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'programs'
        unique_together = ('code', 'college')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(models.Model):
    code = models.CharField(max_length=50)  # e.g., "CS101"
    name = models.CharField(max_length=255)  # e.g., "Data Structures"
    description = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    faculty = models.ForeignKey(User, on_delete=models.PROTECT, related_name='taught_courses',
                               limit_choices_to={'role': 'faculty'})
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    credits = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'courses'
        unique_together = ('code', 'program')
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments',
                               limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ], default='active')
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code}"


# ======================
# Session & Attendance
# ======================

class ClassSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    faculty = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sessions_conducted',
                               limit_choices_to={'role': 'faculty'})
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    topic = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    session_notes = models.TextField(blank=True)  # Renamed from 'notes' to avoid conflict
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'class_sessions'
        ordering = ['-session_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.session_date.strftime('%Y-%m-%d %H:%M')}"


class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='attendance')
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    active_minutes = models.IntegerField(default=0)  # Minutes with focus
    total_minutes = models.IntegerField(default=0)   # Total session minutes
    attendance_percentage = models.FloatField(default=0.0, 
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attendance'
        unique_together = ('student', 'session')
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.session} ({self.status})"


# ======================
# Focus & Violations
# ======================

class FocusLog(models.Model):
    EVENT_TYPES = [
        ('focus_gained', 'Focus Gained'),
        ('focus_lost', 'Focus Lost'),
        ('fullscreen_exit', 'Fullscreen Exit'),
        ('alt_tab', 'Alt+Tab'),
        ('app_switch', 'App Switch'),
        ('minimized', 'Window Minimized'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_logs',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='focus_logs')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)  # Additional info
    
    class Meta:
        db_table = 'focus_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['student', 'session', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.event_type} ({self.timestamp})"


class Violation(models.Model):
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=100)  # e.g., "fullscreen_exit", "copy_paste"
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='medium')
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'violations'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['student', 'session']),
            models.Index(fields=['is_resolved', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.violation_type} ({self.severity})"


# ======================
# Content & Materials
# ======================

class Slide(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='slides')
    slide_number = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()  # OCR'd text from PPT/PDF
    image_url = models.URLField(null=True, blank=True)
    file = models.FileField(upload_to='slides/', null=True, blank=True)
    ai_summary = models.TextField(blank=True)  # Pre-generated by AI
    ai_definitions = models.JSONField(default=list, blank=True)  # List of key terms
    ai_questions = models.JSONField(default=list, blank=True)  # Probable exam questions
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'slides'
        unique_together = ('session', 'slide_number')
        ordering = ['slide_number']
    
    def __str__(self):
        return f"{self.session} - Slide {self.slide_number}"


class Note(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='notes')
    slide = models.ForeignKey(Slide, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()  # Markdown-formatted
    tags = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.title}"


# ======================
# Doubts & AI Responses
# ======================

class Doubt(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('answered', 'Answered'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='doubts')
    question = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    asked_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'doubts'
        ordering = ['-asked_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.question[:50]}"


class DoubtResponse(models.Model):
    doubt = models.OneToOneField(Doubt, on_delete=models.CASCADE, related_name='response')
    answer = models.TextField()
    source_slide = models.ForeignKey(Slide, on_delete=models.SET_NULL, null=True, blank=True)
    source_snippet = models.TextField(blank=True)
    confidence_score = models.FloatField(default=0.0, 
                                         validators=[MinValueValidator(0), MaxValueValidator(1)])
    generated_by_ai = models.BooleanField(default=True)
    faculty_verified = models.BooleanField(default=False)
    responded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'doubt_responses'
    
    def __str__(self):
        return f"Response to: {self.doubt.question[:50]}"


# ======================
# Assessments
# ======================

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    max_score = models.FloatField(default=100.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assignments'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions',
                               limit_choices_to={'role': 'student'})
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'submissions'
        unique_together = ('student', 'assignment')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


# ======================
# Analytics & Reports
# ======================

class SessionReport(models.Model):
    session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='report')
    total_students = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    average_attendance_percentage = models.FloatField(default=0.0)
    violation_count = models.IntegerField(default=0)
    focus_duration_minutes = models.IntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'session_reports'
    
    def __str__(self):
        return f"Report: {self.session}"


class StudentPerformance(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='performance',
                                  limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='performance')
    total_attendance_percentage = models.FloatField(default=0.0)
    average_assignment_score = models.FloatField(default=0.0)
    violation_count = models.IntegerField(default=0)
    total_focus_hours = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_performance'
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"Performance: {self.student.username} - {self.course.code}"


# ======================
# Compiler & Code Execution
# ======================

class CompilerSubmission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('executed', 'Executed'),
        ('failed', 'Failed'),
        ('timeout', 'Timeout'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compiler_submissions',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='compiler_submissions')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    execution_time = models.FloatField(default=0.0)  # In seconds
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'compiler_submissions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'session']),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.language} ({self.status})"


class ScreenLock(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='screen_locks',
                               limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='screen_locks')
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                  related_name='screen_locks_initiated',
                                  limit_choices_to={'role': 'faculty'})
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(auto_now_add=True)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'screen_locks'
        ordering = ['-locked_at']
    
    def __str__(self):
        return f"{'Locked' if self.is_locked else 'Unlocked'} - {self.student.username}"

