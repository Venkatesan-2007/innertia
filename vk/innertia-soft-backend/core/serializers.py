from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import (
    College, Program, Course, Enrollment, ClassSession, Attendance,
    FocusLog, Violation, Slide, Note, Doubt, DoubtResponse, Assignment,
    Submission, SessionReport, StudentPerformance, CompilerSubmission, ScreenLock
)

User = get_user_model()


# ======================
# Auth Serializers
# ======================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_data'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'college': user.college_id,
            'phone': user.phone
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'college', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def validate_role(self, value):
        if value not in ['admin', 'faculty', 'student']:
            raise serializers.ValidationError("Invalid role")
        return value
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# ======================
# Institution Serializers
# ======================

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name', 'code', 'address', 'city', 'country', 'admin', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProgramSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    
    class Meta:
        model = Program
        fields = ['id', 'name', 'code', 'college', 'college_name', 'duration_semesters', 'created_at']
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'program', 'program_name', 
                 'faculty', 'faculty_name', 'semester', 'credits', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_semester(self, value):
        if not (1 <= value <= 8):
            raise serializers.ValidationError("Semester must be between 1 and 8")
        return value
    
    def validate_credits(self, value):
        if not (1 <= value <= 6):
            raise serializers.ValidationError("Credits must be between 1 and 6")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_code', 'enrolled_date', 'status']
        read_only_fields = ['id', 'enrolled_date']


# ======================
# Session & Attendance Serializers
# ======================

class ClassSessionSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = ClassSession
        fields = ['id', 'course', 'course_code', 'faculty', 'faculty_name', 'session_date',
                 'duration_minutes', 'topic', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    session_topic = serializers.CharField(source='session.topic', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'session', 'session_topic', 'status',
                 'active_minutes', 'total_minutes', 'attendance_percentage', 
                 'check_in_time', 'check_out_time', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


# ======================
# Focus & Violation Serializers
# ======================

class FocusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusLog
        fields = ['id', 'student', 'session', 'event_type', 'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']


class ViolationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = Violation
        fields = ['id', 'student', 'student_name', 'session', 'violation_type',
                 'severity', 'description', 'timestamp', 'is_resolved', 'resolution_notes']
        read_only_fields = ['id', 'timestamp']


# ======================
# Content & Material Serializers
# ======================

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['id', 'session', 'slide_number', 'title', 'content', 'image_url',
                 'ai_summary', 'ai_definitions', 'ai_questions', 'created_at']
        read_only_fields = ['id', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'student', 'student_name', 'session', 'slide', 'title',
                 'content', 'tags', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ======================
# Doubt & AI Serializers
# ======================

class DoubtResponseSerializer(serializers.ModelSerializer):
    slide_title = serializers.CharField(source='source_slide.title', read_only=True)
    
    class Meta:
        model = DoubtResponse
        fields = ['id', 'doubt', 'answer', 'source_slide', 'slide_title',
                 'source_snippet', 'confidence_score', 'generated_by_ai',
                 'faculty_verified', 'responded_at']
        read_only_fields = ['id', 'responded_at']


class DoubtSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    response = DoubtResponseSerializer(read_only=True)
    
    class Meta:
        model = Doubt
        fields = ['id', 'student', 'student_name', 'session', 'question', 'status',
                 'asked_at', 'resolved_at', 'response']
        read_only_fields = ['id', 'asked_at']


# ======================
# Assessment Serializers
# ======================

class AssignmentSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'course_code', 'title', 'description', 'due_date',
                 'status', 'max_score', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_max_score(self, value):
        if not (0 < value <= 100):
            raise serializers.ValidationError("Max score must be between 1 and 100")
        return value
    
    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future")
        return value


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'student', 'student_name', 'assignment', 'assignment_title',
                 'content', 'file', 'status', 'score', 'feedback',
                 'submitted_at', 'graded_at']
        read_only_fields = ['id', 'submitted_at']


# ======================
# Analytics Serializers
# ======================

class SessionReportSerializer(serializers.ModelSerializer):
    session_info = ClassSessionSerializer(source='session', read_only=True)
    
    class Meta:
        model = SessionReport
        fields = ['id', 'session', 'session_info', 'total_students', 'present_count',
                 'absent_count', 'average_attendance_percentage', 'violation_count',
                 'focus_duration_minutes', 'generated_at']
        read_only_fields = ['id', 'generated_at']


class StudentPerformanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = StudentPerformance
        fields = ['id', 'student', 'student_name', 'course', 'course_code',
                 'total_attendance_percentage', 'average_assignment_score',
                 'violation_count', 'total_focus_hours', 'last_updated']
        read_only_fields = ['id', 'last_updated']


# ======================
# Compiler & Code Execution Serializers
# ======================

class CompilerSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    session_info = serializers.SerializerMethodField()
    
    class Meta:
        model = CompilerSubmission
        fields = ['id', 'student', 'student_name', 'session', 'session_info',
                 'language', 'code', 'stdout', 'stderr', 'execution_time',
                 'status', 'created_at', 'executed_at']
        read_only_fields = ['id', 'stdout', 'stderr', 'execution_time', 
                           'status', 'created_at', 'executed_at']
    
    def get_session_info(self, obj):
        return {
            'id': obj.session.id,
            'topic': obj.session.topic,
            'course': obj.session.course.code
        }


class ScreenLockSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    locked_by_name = serializers.CharField(source='locked_by.get_full_name', read_only=True)
    
    class Meta:
        model = ScreenLock
        fields = ['id', 'student', 'student_name', 'session', 'locked_by',
                 'locked_by_name', 'is_locked', 'locked_at', 'unlocked_at', 'reason']
        read_only_fields = ['id', 'locked_at', 'unlocked_at']


class ExecuteCodeSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=['python', 'javascript', 'java'])
    code = serializers.CharField()
    session_id = serializers.IntegerField(required=False)
