from . import views
from django.urls import path, include
from .views import HelloAPI, RegistrationAPI, LoginAPI, UserAPI, ProfileUpdateAPI

urlpatterns =[
    path('', UserAPI.as_view()),
    path('login/',LoginAPI.as_view()),
    path('signup/', RegistrationAPI.as_view()),
    path("profile/<int:user_pk>/update/", ProfileUpdateAPI.as_view())
    # path('tech/', views.TechView.as_view(), name="tech")
 ]
