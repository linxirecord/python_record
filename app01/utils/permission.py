from rest_framework.permissions import BasePermission
class Admimpermission(BasePermission):
    ''' Return `True` if permission is granted, `False` otherwise.'''
    def has_permission(self,request,view):
        if request.user.user_type !=2 :
            return False
        return True

class Ordinarypermission(BasePermission):
    ''' Return `True` if permission is granted, `False` otherwise.'''
    def has_permission(self,request,view):
        if request.user.user_type >2:
            return False
        return True



