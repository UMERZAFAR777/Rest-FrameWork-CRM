from django.contrib import admin
from django.urls import path,include
from account.views import *
from account import views
urlpatterns = [
    path('register/',RegisterForm.as_view(),name='register'),
    path('loginform/',LoginForm.as_view(),name='loginform'),
    path('profileform/',ProfileForm.as_view(),name='profileform'),
    path('changepasswordform/',ChangePasswordForm.as_view(),name='changepasswordform'),
    path('restmailform/',ResetMailForm.as_view(),name='restmailform'),
    path('resetpasswordform/<str:uid>/<str:token>/', ResetPasswordForm.as_view(), name='reset_password_form'),
]

















