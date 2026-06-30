from rest_framework.permissions import BasePermission

class HasRequiredPermission(BasePermission):
    """
    A dynamic permission guard. Checks if the incoming JWT contains the required action.
    """
    def __init__(self, required_permission):
        self.required_permission = required_permission

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'role', None) == "ADMIM":
            return True

        return request.user.has_perm(self.required_permission)

# Helper function to generate permissions cleanly inside decorators
def require_permission(permission_name):
    class FormattedPermission(HasRequiredPermission):
        def __init__(self):
            super().__init__(permission_name)
    return FormattedPermission