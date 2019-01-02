from .models import UserInfo
from rest_framework import viewsets
from app01.serializers import UserSerializer
from app01 import models
import json
from rest_framework.views import APIView
from django.http import JsonResponse
from app01.utils.permission import  Ordinarypermission
from app01.utils.authenticate import Authtication


def md5(user):
    '''create token'''
    import hashlib,time
    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

def check_user(self,request,user,pwd):
    '''check 'username' and 'password',write 'token' in 'UserToken' and return info for web '''
    ret={'code':1000,'msg':None}
    try:
        userset=UserInfo.objects.filter(username=user,password=pwd).first()
        print(userset)
        if not userset:
            ret['code']=1001
            ret['msg']='Username or password is error'
        else:
            token=md5(user)
            models.UserToken.objects.update_or_create(user=userset,defaults={"token":token})
            ret['token']=token
    except Exception as e:
        ret['code']=1002
        ret['msg']=" exception request"
    return (ret)


class UserViewSet(viewsets.ModelViewSet):
    '''serializing one of those instances and redo create and check data'''
    authentication_classes = []
    queryset=UserInfo.objects.all()
    serializer_class = UserSerializer
    def create(self,request,*args,**kwargs):
        '''redo create'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['username']
        pwd = serializer.data['password']
        re_data=check_user(self,request,user,pwd)
        re_data=json.dumps(re_data)
        return JsonResponse(re_data,safe=False)

###########登录成功后的数据处理#############

data_dict={
    1:{ 'name':'xiaowang',
    'age':18,
    'sex':'M',
      },
}

class InfoViewSet(APIView):
    '''return data for successful'''
    authentication_classes = [Authtication,]
    permission_classes = [Ordinarypermission,]
    def get(self,request,*args,**kwargs):
        ret={'code':1000,'msg':None,'data':None,'access':None}
        try:
            ret['data']=data_dict
            ret['access']=(1,2)
        except Exception as e:
            pass
        return JsonResponse (ret)
    
