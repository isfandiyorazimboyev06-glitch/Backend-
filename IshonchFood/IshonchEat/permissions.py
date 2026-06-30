from rest_framework.permissions import BasePermission

class HasRequiredPermission(BasePermission):
    """
    A dynamic permission guard. Checks if the incoming JWT contains the required action.
    """
    def __init__(self, required_permission):
        self.required_permission = required_permission

    def has_permission(self, request, view):
        # 1. Guard against unauthenticated users
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Fix typo: "ADMIN" instead of "ADMIM"
        if getattr(request.user, 'role', None) == "ADMIN":
            return True

        # 3. Fallback to token array authorization strings check
        return request.user.has_perm(self.required_permission)

# Helper function to generate permissions cleanly inside decorators
def require_permission(permission_name):
    """
    Helper decorator function to generate permission classes cleanly inside DRF decorators.
    Usage: @permission_classes([require_permission('menu.manage')])
    """
    class FormattedPermission(HasRequiredPermission):
        def __init__(self):
            super().__init__(permission_name)
    return FormattedPermission