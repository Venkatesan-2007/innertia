from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q, Avg
from django.db import models
import subprocess
import json
from .models import (
    College, Program, Course, Enrollment, ClassSession, Attendance,
    FocusLog, Violation, Slide, Note, Doubt, DoubtResponse, Assignment,
    Submission, SessionReport, StudentPerformance, CompilerSubmission, ScreenLock
)
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer, UserRegistrationSerializer,
    CollegeSerializer, ProgramSerializer, CourseSerializer, EnrollmentSerializer,
    ClassSessionSerializer, AttendanceSerializer, FocusLogSerializer, ViolationSerializer,
    SlideSerializer, NoteSerializer, DoubtSerializer, DoubtResponseSerializer,
    AssignmentSerializer, SubmissionSerializer, SessionReportSerializer,
    StudentPerformanceSerializer, CompilerSubmissionSerializer, ScreenLockSerializer,
    ExecuteCodeSerializer
)
from .permissions import (
    IsSuperAdmin, IsCollegeAdmin, IsFaculty, IsFacultyOrAdmin, IsStudent,
    IsOwnerOrAdmin, IsOwner, CanManageEnrollment, CanMarkAttendance, CanViewSession
)
from .filters import (
    CollegeFilter, ProgramFilter, CourseFilter, EnrollmentFilter,
    ClassSessionFilter, AttendanceFilter, ViolationFilter, FocusLogFilter,
    SlideFilter, NoteFilter, DoubtFilter, AssignmentFilter, SubmissionFilter,
    StudentPerformanceFilter
)

User = get_user_model()


# ======================
# Auth Views
# ======================

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'register':
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return UserRegistrationSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================
# Institution ViewSets
# ======================

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CollegeFilter
    search_fields = ['name', 'code', 'city']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSuperAdmin()]
        return [permissions.IsAuthenticated()]


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProgramFilter
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'semester', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'enrolled_students']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['enroll_student']:
            return [IsFacultyOrAdmin()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def enroll_student(self, request, pk=None):
        """Enroll a student in a course"""
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response(
                {'detail': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response(
                {'detail': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course
        )
        
        serializer = EnrollmentSerializer(enrollment)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    
    @action(detail=True, methods=['get'])
    def enrolled_students(self, request, pk=None):
        """Get all enrolled students in a course"""
        course = self.get_object()
        enrollments = course.enrollments.filter(status='active')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EnrollmentFilter
    search_fields = ['student__username', 'course__code']
    ordering_fields = ['enrolled_date', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student=user)
        elif user.role == 'faculty':
            return Enrollment.objects.filter(course__faculty=user)
        return Enrollment.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanManageEnrollment()]
        return [permissions.IsAuthenticated()]


# ======================
# Session & Attendance ViewSets
# ======================

class ClassSessionViewSet(viewsets.ModelViewSet):
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClassSessionFilter
    search_fields = ['topic', 'description']
    ordering_fields = ['-session_date', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'faculty':
            return ClassSession.objects.filter(faculty=user)
        elif user.role == 'student':
            # Student can only see sessions for their enrolled courses
            return ClassSession.objects.filter(
                course__enrollments__student=user,
                course__enrollments__status='active'
            ).distinct()
        return ClassSession.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'attendance_report']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['start_session', 'end_session']:
            return [IsFacultyOrAdmin()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def start_session(self, request, pk=None):
        """Start a class session"""
        session = self.get_object()
        session.status = 'active'
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End a class session"""
        session = self.get_object()
        session.status = 'completed'
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance_report(self, request, pk=None):
        """Get attendance report for a session"""
        session = self.get_object()
        attendance = session.attendance.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AttendanceFilter
    ordering_fields = ['-check_in_time', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Attendance.objects.filter(student=user)
        elif user.role == 'faculty':
            return Attendance.objects.filter(session__faculty=user)
        return Attendance.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'mark_attendance':
            return [CanMarkAttendance()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [CanMarkAttendance()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        """Mark or update attendance"""
        student_id = request.data.get('student_id')
        session_id = request.data.get('session_id')
        status_val = request.data.get('status', 'present')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            session = ClassSession.objects.get(id=session_id)
        except (User.DoesNotExist, ClassSession.DoesNotExist):
            return Response(
                {'detail': 'Invalid student or session'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        attendance, created = Attendance.objects.update_or_create(
            student=student,
            session=session,
            defaults={
                'status': status_val,
                'check_in_time': timezone.now() if not created else attendance.check_in_time,
            }
        )
        
        # Calculate attendance percentage (>80% is present)
        active_min = attendance.active_minutes
        total_min = session.duration_minutes
        percentage = (active_min / total_min * 100) if total_min > 0 else 0
        attendance.attendance_percentage = percentage
        
        # Auto-set status based on percentage
        if percentage >= 80:
            attendance.status = 'present'
        elif percentage >= 50:
            attendance.status = 'late'
        else:
            attendance.status = 'absent'
        attendance.save()
        
        serializer = self.get_serializer(attendance)
        return Response(serializer.data)


# ======================
# Focus & Violation ViewSets
# ======================

class FocusLogViewSet(viewsets.ModelViewSet):
    queryset = FocusLog.objects.all()
    serializer_class = FocusLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FocusLogFilter
    ordering_fields = ['-timestamp']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return FocusLog.objects.filter(student=user)
        elif user.role == 'faculty':
            return FocusLog.objects.filter(session__faculty=user)
        return FocusLog.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'log_event':
            return [IsStudent()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def log_event(self, request):
        """Log a focus event"""
        request.data['student'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViolationViewSet(viewsets.ModelViewSet):
    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ViolationFilter
    ordering_fields = ['-timestamp', 'severity']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Violation.objects.filter(student=user)
        elif user.role == 'faculty':
            return Violation.objects.filter(session__faculty=user)
        return Violation.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'resolve_violation':
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def resolve_violation(self, request, pk=None):
        """Mark violation as resolved"""
        violation = self.get_object()
        violation.is_resolved = True
        violation.resolution_notes = request.data.get('resolution_notes', '')
        violation.save()
        serializer = self.get_serializer(violation)
        return Response(serializer.data)


# ======================
# Content & Material ViewSets
# ======================

class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SlideFilter
    ordering_fields = ['slide_number']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteFilter
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at', '-updated_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Note.objects.filter(Q(student=user) | Q(is_public=True))
        return Note.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create']:
            return [IsStudent()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]


# ======================
# Doubt & AI ViewSets
# ======================

class DoubtViewSet(viewsets.ModelViewSet):
    queryset = Doubt.objects.all()
    serializer_class = DoubtSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DoubtFilter
    search_fields = ['question', 'subject']
    ordering_fields = ['-created_at', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Doubt.objects.filter(student=user)
        elif user.role == 'faculty':
            return Doubt.objects.filter(session__course__faculty=user)
        return Doubt.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'resolve_doubt']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'ask_doubt':
            return [IsStudent()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def ask_doubt(self, request):
        """Ask a new doubt"""
        request.data['student'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def resolve_doubt(self, request, pk=None):
        """Mark doubt as resolved"""
        doubt = self.get_object()
        doubt.status = 'resolved'
        doubt.resolved_at = timezone.now()
        doubt.save()
        serializer = self.get_serializer(doubt)
        return Response(serializer.data)


class DoubtResponseViewSet(viewsets.ModelViewSet):
    queryset = DoubtResponse.objects.all()
    serializer_class = DoubtResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoubtFilter
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]


# ======================
# Assessment ViewSets
# ======================

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AssignmentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['-due_date', 'status']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsFacultyOrAdmin()]
        return [permissions.IsAuthenticated()]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SubmissionFilter
    ordering_fields = ['-submitted_at', 'status']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Submission.objects.filter(student=user)
        elif user.role == 'faculty':
            return Submission.objects.filter(assignment__course__faculty=user)
        return Submission.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action == 'grade_submission':
            return [IsFacultyOrAdmin()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsStudent()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def grade_submission(self, request, pk=None):
        """Grade a submission"""
        submission = self.get_object()
        score = request.data.get('score')
        feedback = request.data.get('feedback', '')
        
        if score is None:
            return Response(
                {'detail': 'Score is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.score = score
        submission.feedback = feedback
        submission.status = 'graded'
        submission.graded_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)


# ======================
# Analytics ViewSets
# ======================

class SessionReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SessionReport.objects.all()
    serializer_class = SessionReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentPerformanceFilter
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'faculty':
            return SessionReport.objects.filter(session__faculty=user)
        elif user.role == 'student':
            return SessionReport.objects.filter(
                session__course__enrollments__student=user
            )
        return SessionReport.objects.all()
    
    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        """Generate session report"""
        session_id = request.data.get('session_id')
        
        try:
            session = ClassSession.objects.get(id=session_id)
        except ClassSession.DoesNotExist:
            return Response(
                {'detail': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        attendance_records = session.attendance.all()
        total_students = attendance_records.count()
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        
        avg_attendance = (
            attendance_records.aggregate(avg=models.Avg('attendance_percentage'))['avg'] or 0
        )
        
        violation_count = session.violations.count()
        
        report, created = SessionReport.objects.update_or_create(
            session=session,
            defaults={
                'total_students': total_students,
                'present_count': present_count,
                'absent_count': absent_count,
                'average_attendance_percentage': avg_attendance,
                'violation_count': violation_count,
            }
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class StudentPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentPerformance.objects.all()
    serializer_class = StudentPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentPerformanceFilter
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return StudentPerformance.objects.filter(student=user)
        elif user.role == 'faculty':
            return StudentPerformance.objects.filter(course__faculty=user)
        return StudentPerformance.objects.all()


# ======================
# Compiler & Code Execution Views
# ======================

class CompileCodeView(viewsets.ViewSet):
    """Execute code in sandbox environment"""
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    @action(detail=False, methods=['post'])
    def execute(self, request):
        """Execute code and return output"""
        serializer = ExecuteCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        language = serializer.validated_data['language']
        code = serializer.validated_data['code']
        session_id = serializer.validated_data.get('session_id')
        
        # Language-specific timeouts and run commands
        timeouts = {
            'python': 15,
            'javascript': 10,
            'java': 20,
        }
        
        timeout = timeouts.get(language, 10)
        
        try:
            # Simple subprocess execution with timeout
            # For production, use proper sandbox like Judge0 API
            if language == 'python':
                result = subprocess.run(
                    ['python', '-c', code],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            elif language == 'javascript':
                result = subprocess.run(
                    ['node', '-e', code],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            elif language == 'java':
                # Java execution would require compilation first
                # For simplicity, we're not supporting interactive Java execution
                return Response(
                    {'error': 'Java execution not yet supported'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Store submission if session_id provided
            if session_id:
                try:
                    session = ClassSession.objects.get(id=session_id)
                    CompilerSubmission.objects.create(
                        student=request.user,
                        session=session,
                        language=language,
                        code=code,
                        stdout=result.stdout,
                        stderr=result.stderr,
                        execution_time=result.returncode == 0,
                        status='executed' if result.returncode == 0 else 'failed'
                    )
                except ClassSession.DoesNotExist:
                    pass
            
            return Response({
                'language': language,
                'code': code,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exitcode': result.returncode,
                'status': 'executed' if result.returncode == 0 else 'failed'
            })
        
        except subprocess.TimeoutExpired:
            return Response({
                'error': f'Code execution timeout (limit: {timeout}s)',
                'language': language,
                'status': 'timeout'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompilerSubmissionViewSet(viewsets.ModelViewSet):
    """Manage code submissions"""
    queryset = CompilerSubmission.objects.all()
    serializer_class = CompilerSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'session', 'language', 'status']
    ordering_fields = ['-created_at', 'language']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return CompilerSubmission.objects.filter(student=user)
        elif user.role == 'faculty':
            return CompilerSubmission.objects.filter(session__faculty=user)
        return CompilerSubmission.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ScreenLockViewSet(viewsets.ModelViewSet):
    """Manage screen locks for students"""
    queryset = ScreenLock.objects.all()
    serializer_class = ScreenLockSerializer
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'session', 'is_locked']
    ordering_fields = ['-locked_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'faculty':
            return ScreenLock.objects.filter(session__faculty=user)
        return ScreenLock.objects.all()
    
    @action(detail=False, methods=['post'])
    def lock_screen(self, request):
        """Lock a student's screen during session"""
        student_id = request.data.get('student_id')
        session_id = request.data.get('session_id')
        reason = request.data.get('reason', '')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            session = ClassSession.objects.get(id=session_id, faculty=request.user)
        except (User.DoesNotExist, ClassSession.DoesNotExist):
            return Response(
                {'error': 'Student or session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Unlock any existing locks for this student in this session
        ScreenLock.objects.filter(
            student=student,
            session=session,
            is_locked=True
        ).update(is_locked=False, unlocked_at=timezone.now())
        
        # Create new lock
        lock = ScreenLock.objects.create(
            student=student,
            session=session,
            locked_by=request.user,
            is_locked=True,
            reason=reason
        )
        
        serializer = self.get_serializer(lock)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def unlock_screen(self, request):
        """Unlock a student's screen"""
        student_id = request.data.get('student_id')
        session_id = request.data.get('session_id')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            session = ClassSession.objects.get(id=session_id, faculty=request.user)
            lock = ScreenLock.objects.get(
                student=student,
                session=session,
                is_locked=True
            )
        except (User.DoesNotExist, ClassSession.DoesNotExist, ScreenLock.DoesNotExist):
            return Response(
                {'error': 'Lock not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        lock.is_locked = False
        lock.unlocked_at = timezone.now()
        lock.save()
        
        serializer = self.get_serializer(lock)
        return Response(serializer.data)

