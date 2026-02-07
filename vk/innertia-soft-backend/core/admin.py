from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, College, Program, Course, Enrollment, ClassSession, Attendance,
    FocusLog, Violation, Slide, Note, Doubt, DoubtResponse, Assignment,
    Submission, SessionReport, StudentPerformance
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Role & Institution', {'fields': ('role', 'college', 'profile_picture')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'role', 'college', 'is_staff')
    list_filter = ('role', 'is_staff', 'college', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'country', 'admin')
    list_filter = ('city', 'country', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'college', 'duration_semesters')
    list_filter = ('college', 'duration_semesters', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'program', 'faculty', 'semester', 'credits')
    list_filter = ('program', 'faculty', 'semester', 'created_at')
    search_fields = ('code', 'name')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_date')
    list_filter = ('course', 'status', 'enrolled_date')
    search_fields = ('student__username', 'course__code')


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'faculty', 'session_date', 'topic', 'status')
    list_filter = ('course', 'faculty', 'status', 'session_date')
    search_fields = ('topic', 'course__code')
    ordering = ('-session_date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'attendance_percentage', 'recorded_at')
    list_filter = ('status', 'session__course', 'recorded_at')
    search_fields = ('student__username', 'session__topic')
    readonly_fields = ('recorded_at', 'attendance_percentage')
    ordering = ('-recorded_at',)


@admin.register(FocusLog)
class FocusLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'event_type', 'timestamp')
    list_filter = ('event_type', 'session__course', 'timestamp')
    search_fields = ('student__username', 'event_type')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'violation_type', 'severity', 'is_resolved', 'timestamp')
    list_filter = ('severity', 'is_resolved', 'violation_type', 'timestamp')
    search_fields = ('student__username', 'violation_type', 'description')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('session', 'slide_number', 'title')
    list_filter = ('session__course', 'session__session_date')
    search_fields = ('title', 'content')
    ordering = ('session', 'slide_number')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'title', 'is_public', 'created_at')
    list_filter = ('is_public', 'session__course', 'created_at', 'updated_at')
    search_fields = ('student__username', 'title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'asked_at')
    list_filter = ('status', 'session__course', 'asked_at')
    search_fields = ('student__username', 'question')
    readonly_fields = ('asked_at',)
    ordering = ('-asked_at',)


@admin.register(DoubtResponse)
class DoubtResponseAdmin(admin.ModelAdmin):
    list_display = ('doubt', 'source_slide', 'confidence_score', 'generated_by_ai', 'faculty_verified')
    list_filter = ('generated_by_ai', 'faculty_verified', 'responded_at')
    search_fields = ('doubt__question', 'answer')
    readonly_fields = ('responded_at',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'due_date', 'status', 'max_score')
    list_filter = ('course', 'status', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-due_date',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'assignment__course', 'submitted_at', 'graded_at')
    search_fields = ('student__username', 'assignment__title')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(SessionReport)
class SessionReportAdmin(admin.ModelAdmin):
    list_display = ('session', 'total_students', 'present_count', 'average_attendance_percentage', 'violation_count')
    list_filter = ('session__course', 'generated_at')
    search_fields = ('session__topic',)
    readonly_fields = ('generated_at',)


@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'total_attendance_percentage', 'average_assignment_score', 'violation_count')
    list_filter = ('course', 'last_updated')
    search_fields = ('student__username', 'course__code')
    readonly_fields = ('last_updated',)

