from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    # 로드맵 추가도 post로하고, 조회는 get으로,
    # 경로도 root 경로로 변경하자
    path('add/', views.add_roadmap)

 ]
