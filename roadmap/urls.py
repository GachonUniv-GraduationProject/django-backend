from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('add/', views.add_roadmap)

 ]
