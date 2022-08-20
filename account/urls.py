from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('signup/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('check/', views.check_users),
    path('logintest/', views.logintest),
    path('signuptest/', views.signuptest)

 ]
