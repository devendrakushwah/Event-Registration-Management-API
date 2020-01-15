from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('auth/generate_user_token', obtain_auth_token),
    path('auth/get_my_info', MyInfoView.as_view()),
    path('auth/signup', SignUpView.as_view()),
]