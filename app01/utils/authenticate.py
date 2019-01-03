from app01 import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from datetime import timedelta
import time,datetime
class Authtication(BaseAuthentication):
    '''when clients login again that checks token and expire date'''
    def authenticate(self,request):
        token=request._request.GET.get('token')
        token_obj=models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('Authentication failed')
        return self.authenticate_credentials(token_obj.token)

    def authenticate_header(self,request):
        pass

    def authenticate_credentials(self,key):
        '''expire date'''
        try:
            token_obj = models.UserToken.objects.filter(token=key).first()
        except:
            raise exceptions.AuthenticationFailed(('Invalid token.'))
        if datetime.datetime.now()>(token_obj.token_created+timedelta(seconds=200)).replace(tzinfo=None):
            raise   exceptions.AuthenticationFailed(('Token has expired'))
        return (token_obj.user,token_obj)
