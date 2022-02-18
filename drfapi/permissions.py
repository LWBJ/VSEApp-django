from rest_framework import permissions

class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        return ( obj.owner == request.user )
        
class UserOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): 
        return ( obj == request.user )
        
class UnauthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view): 
        return not(request.user.is_authenticated)