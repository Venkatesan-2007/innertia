import django_filters
from rest_framework import filters
from django.db.models import Q
from .models import (
    College, Program, Course, Enrollment, ClassSession, Attendance,
    FocusLog, Violation, Slide, Note, Doubt, DoubtResponse, Assignment,
    Submission, StudentPerformance
)


class CollegeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = College
        fields = ['city', 'country']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(code__icontains=value))


class ProgramFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Program
        fields = ['college']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(code__icontains=value))


class CourseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    semester = django_filters.NumberFilter()
    credits = django_filters.NumberFilter()
    
    class Meta:
        model = Course
        fields = ['program', 'faculty', 'semester', 'credits']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | 
            Q(code__icontains=value) | 
            Q(description__icontains=value)
        )


class EnrollmentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ])
    
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']


class ClassSessionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    session_date_from = django_filters.DateFilter(
        field_name='session_date', 
        lookup_expr='gte'
    )
    session_date_to = django_filters.DateFilter(
        field_name='session_date', 
        lookup_expr='lte'
    )
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = ClassSession
        fields = ['course', 'status', 'session_date_from', 'session_date_to']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(topic__icontains=value) | 
            Q(description__icontains=value)
        )


class AttendanceFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ])
    session = django_filters.ModelChoiceFilter(queryset=ClassSession.objects.all())
    
    class Meta:
        model = Attendance
        fields = ['student', 'session', 'status']


class ViolationFilter(django_filters.FilterSet):
    status = django_filters.BooleanFilter(field_name='is_resolved')
    severity = django_filters.ChoiceFilter(choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    violation_type = django_filters.CharFilter()
    timestamp_from = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte'
    )
    timestamp_to = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Violation
        fields = ['student', 'session', 'violation_type', 'severity', 'status']


class FocusLogFilter(django_filters.FilterSet):
    event_type = django_filters.ChoiceFilter(choices=[
        ('focus_gained', 'Focus Gained'),
        ('focus_lost', 'Focus Lost'),
        ('fullscreen_exit', 'Fullscreen Exit'),
        ('alt_tab', 'Alt+Tab'),
        ('app_switch', 'App Switch'),
        ('minimized', 'Window Minimized'),
    ])
    timestamp_from = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte'
    )
    timestamp_to = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte'
    )
    
    class Meta:
        model = FocusLog
        fields = ['student', 'session', 'event_type']


class SlideFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Slide
        fields = ['session']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(notes__icontains=value))


class NoteFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    is_public = django_filters.BooleanFilter()
    
    class Meta:
        model = Note
        fields = ['student', 'is_public']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(content__icontains=value)
        )


class DoubtFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('open', 'Open'),
        ('answered', 'Answered'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ])
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Doubt
        fields = ['student', 'session', 'status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(question__icontains=value) | 
            Q(subject__icontains=value)
        )


class AssignmentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ])
    due_date_from = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='gte'
    )
    due_date_to = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='lte'
    )
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Assignment
        fields = ['course', 'status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(description__icontains=value)
        )


class SubmissionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
        ('draft', 'Draft'),
    ])
    
    class Meta:
        model = Submission
        fields = ['student', 'assignment', 'status']


class StudentPerformanceFilter(django_filters.FilterSet):
    class Meta:
        model = StudentPerformance
        fields = ['student', 'course']
