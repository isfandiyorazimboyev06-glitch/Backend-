from rest_framework import permissions

class HasMenuManagePermission(permissions.BasePermission):
    """
    Token ichida permissions ro'yxatida 'menu.manage' borligini tekshiradi.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # SimpleJWT tokendan kelgan payloadni request.auth orqali o'qiymiz
        token_permissions = request.auth.get('permissions', [])
        return 'menu.manage' in token_permissions



class IsRestaurantOwner(permissions.BasePermission):
    """
    Restoran egasi aynan shu token egasi ekanligini tekshiradi.
    """
    def has_object_permission(self, request, view, obj):
        # Agar so'rov ob'ekt darajasida bo'lsa (PUT, PATCH, DELETE)
        # Token ichidagi 'user_id' ob'ektdagi 'owner_user_id' ga teng bo'lishi shart
        token_user_id = str(request.auth.get('user_id'))
        
        if hasattr(obj, 'owner_user_id'):
            return obj.owner_user_id == token_user_id
        elif hasattr(obj, 'restaurant'):
            return obj.restaurant.owner_user_id == token_user_id
            
        return False