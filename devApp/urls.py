from django.urls import path
from devApp import views
urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/', views.read),
    path('add/', views.add),
    path('test/', views.test_read),
    path('json/', views.json_test),
    path('person/add/', views.json_add),
    path('find/', views.json_find),
    path('person/', views.json_test)

]
