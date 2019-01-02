from rest_framework import serializers
from .models import UserInfo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_type=serializers.CharField(source="get_user_type_display")
    class Meta:
        model = UserInfo
        fields = ('id','user_type','username','password')


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    user_type=serializers.CharField(source="UserInfo.user_type")
    username=serializers.CharField(source="UserInfo.username")
    password=serializers.CharField(source="UserInfo.password")
    class Meta:
        model = UserInfo
        fields = ('id','user_type','username','password','token')
