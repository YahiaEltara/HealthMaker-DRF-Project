from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsClientOrAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users have full access.
    - Clients can perform any request method (full access).
    - Coaches are restricted to SAFE_METHODS (GET, OPTIONS, HEAD).
    - Other users have no access.
    """
    def has_permission(self, request, view):
        # Admin users always have full access
        if request.user.is_staff:
            return True

        # Clients have full access to any request method
        if hasattr(request.user, 'client'):
            return True

        # Coaches are restricted to safe methods only
        if hasattr(request.user, 'coach'):
            return request.method in SAFE_METHODS

        # Other users are denied access
        return False

    def has_object_permission(self, request, view, obj):
        # Admin users always have full access
        if request.user.is_staff:
            return True

        # Clients can access any object
        if hasattr(request.user, 'client'):
            return True

        # Coaches are restricted to safe methods only
        if hasattr(request.user, 'coach'):
            return request.method in SAFE_METHODS

        # Other users are denied access
        return False
    



class IsCoachOrAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users have full access.
    - Coaches can perform any request method (full access).
    - Clients are restricted to SAFE_METHODS (GET, OPTIONS, HEAD).
    - Other users have no access.
    """
    def has_permission(self, request, view):
        # Admin users always have full access
        if request.user.is_staff:
            return True

        # Coaches have full access to any request method
        if hasattr(request.user, 'coach'):
            return True

        # Clients are restricted to safe methods only
        if hasattr(request.user, 'client'):
            return request.method in SAFE_METHODS

        # Other users are denied access
        return False

    def has_object_permission(self, request, view, obj):
        # Admin users always have full access
        if request.user.is_staff:
            return True

        # Coaches can access any object
        if hasattr(request.user, 'coach'):
            return True

        # Clients are restricted to safe methods only
        if hasattr(request.user, 'client'):
            return request.method in SAFE_METHODS

        # Other users are denied access
        return False

