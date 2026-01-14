from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Only allow users in Admin group."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsInstructor(BasePermission):
    """Only allow users in Instructor group."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Instructor').exists()

class IsStudent(BasePermission):
    """Only allow users in Student group."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Student').exists()

class IsSponsor(BasePermission):
    """Only allow users in Sponsor group."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sponsor').exists()
