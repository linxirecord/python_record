from app01 import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

class Authtication(BaseAuthentication):
    '''when clients login again that checks token'''
    def authenticate(self,request):
        token=request._request.GET.get('token')
        token_obj=models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('Authentication failed')
        return (token_obj.user,token_obj)

    def authenticate_header(self,request):
        pass