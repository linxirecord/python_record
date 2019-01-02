from django.db import models

user_type_choice=(
    (1,"ordinaryuser"),
    (2,"adminuser"),
)

class UserInfo(models.Model):
    '''definite table'''
    #user_type=models.IntegerField(choices=user_type_choice)
    user_type=models.IntegerField(choices=user_type_choice)
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64)


class UserToken(models.Model):
    '''definite table'''
    user=models.OneToOneField(UserInfo,on_delete=models.CASCADE)
    token=models.CharField(max_length=64)
