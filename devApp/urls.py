from django.urls import path
from devApp import views
urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read),
    path('add/<name>/<content>/', views.add),
    path('test/', views.test_read)
]
