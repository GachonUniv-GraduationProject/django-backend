from django.urls import path, include

from core import views
urlpatterns = [
    path('', views.index),
    path('login/', include("login.urls"))



]
