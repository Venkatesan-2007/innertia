from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, UserViewSet,
    CollegeViewSet, ProgramViewSet, CourseViewSet, EnrollmentViewSet,
    ClassSessionViewSet, AttendanceViewSet,
    FocusLogViewSet, ViolationViewSet,
    SlideViewSet, NoteViewSet,
    DoubtViewSet, DoubtResponseViewSet,
    AssignmentViewSet, SubmissionViewSet,
    SessionReportViewSet, StudentPerformanceViewSet,
    CompileCodeView, CompilerSubmissionViewSet, ScreenLockViewSet
)

router = DefaultRouter()

# Auth routes
router.register(r'users', UserViewSet, basename='user')

# Institution routes
router.register(r'colleges', CollegeViewSet, basename='college')
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

# Session & Attendance routes
router.register(r'sessions', ClassSessionViewSet, basename='session')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# Focus & Violation routes
router.register(r'focus-logs', FocusLogViewSet, basename='focus-log')
router.register(r'violations', ViolationViewSet, basename='violation')

# Content routes
router.register(r'slides', SlideViewSet, basename='slide')
router.register(r'notes', NoteViewSet, basename='note')

# Doubt & AI routes
router.register(r'doubts', DoubtViewSet, basename='doubt')
router.register(r'doubt-responses', DoubtResponseViewSet, basename='doubt-response')

# Assessment routes
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', SubmissionViewSet, basename='submission')

# Analytics routes
router.register(r'session-reports', SessionReportViewSet, basename='session-report')
router.register(r'student-performance', StudentPerformanceViewSet, basename='student-performance')

# Compiler & Execution routes
router.register(r'compiler-submissions', CompilerSubmissionViewSet, basename='compiler-submission')
router.register(r'screen-locks', ScreenLockViewSet, basename='screen-lock')
router.register(r'compile', CompileCodeView, basename='compile')

urlpatterns = [
    # Auth endpoints
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API routes
    path('', include(router.urls)),
]
