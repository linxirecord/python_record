from app01.views import UserViewSet,InfoViewSet
from rest_framework import renderers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
login_list=UserViewSet.as_view(
    {
        'get':'list',
        'post':'create',
    }
)


urlpatterns = format_suffix_patterns([
   path('login/', login_list, name='login_list'),
])