from django.urls import path
from crawling import views

urlpatterns = [
    path('recruit/', views.recruit_json)
]