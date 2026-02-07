from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to super admin users (role='admin').
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsCollegeAdmin(permissions.BasePermission):
    """
    Allows access only to college admin users managing their own college.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
    
    def has_object_permission(self, request, view, obj):
        # If user is super admin, allow
        if request.user.role == 'admin':
            # Check if managing own college
            return (
                (hasattr(obj, 'college') and obj.college == request.user.college) or
                (hasattr(obj, 'admin') and obj.admin == request.user)
            )
        return False


class IsFaculty(permissions.BasePermission):
    """
    Allows access only to faculty users (role='faculty').
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'faculty'
        )


class IsFacultyOrAdmin(permissions.BasePermission):
    """
    Allows access to faculty or admin users.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['faculty', 'admin']
        )


class IsStudent(permissions.BasePermission):
    """
    Allows access only to student users (role='student').
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access to object owner or admin users.
    Expects model to have 'user' or 'student' field.
    """
    def has_object_permission(self, request, view, obj):
        # Admin always has access
        if request.user.role == 'admin':
            return True
        
        # Owner has access
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        
        return False


class IsOwner(permissions.BasePermission):
    """
    Allows access only to the object owner (user or student field).
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'student'):
            return obj.student == request.user
        
        return False


class CanManageEnrollment(permissions.BasePermission):
    """
    Allows college admin to manage enrollments in their college,
    or students to view their own enrollments.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin of the college can manage
        if request.user.role == 'admin':
            return obj.course.program.college == request.user.college
        
        # Student can view/modify own enrollment
        if request.user.role == 'student':
            return obj.student == request.user
        
        # Faculty can view enrollments in their course
        if request.user.role == 'faculty':
            return obj.course.faculty == request.user
        
        return False


class CanMarkAttendance(permissions.BasePermission):
    """
    Allows faculty to mark attendance for their sessions.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['faculty', 'admin']
        )
    
    def has_object_permission(self, request, view, obj):
        # Admin can mark any attendance
        if request.user.role == 'admin':
            return True
        
        # Faculty can mark attendance for their sessions
        if request.user.role == 'faculty':
            return obj.session.course.faculty == request.user
        
        return False


class CanViewSession(permissions.BasePermission):
    """
    Allows faculty to view their sessions,
    students to view sessions they're enrolled in.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Faculty can view their sessions
        if request.user.role == 'faculty':
            return obj.course.faculty == request.user
        
        # Student can view sessions for their enrolled courses
        if request.user.role == 'student':
            return Enrollment.objects.filter(
                student=request.user,
                course=obj.course,
                status='active'
            ).exists()
        
        # Admin can view all
        if request.user.role == 'admin':
            return True
        
        return False


# Import here to avoid circular imports
from core.models import Enrollment
