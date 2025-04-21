from rest_framework import permissions

class IsInterviewerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow interviewers or admins to access interview resources.
    """
    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Allow full access for staff and interviewers
        return request.user and (
            request.user.is_staff or
            hasattr(request.user, 'interviewer_profile')
        )

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for the candidate and interviewer
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated and
                (
                    request.user == obj.interviewer or
                    request.user == obj.candidate.user
                )
            )
        
        # Allow full access for staff and the assigned interviewer
        return (
            request.user.is_staff or
            request.user == obj.interviewer
        ) 