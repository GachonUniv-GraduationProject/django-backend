from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('signup/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('check/', views.check_users),
    path('logintest/', views.login_test),
    path('signuptest/', views.signup_test),
    path('addtech/', views.add_tech_stack),
    # path('', views.user_check)

 ]
