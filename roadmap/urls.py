from django.urls import path, include
from . import views
from rest_framework import urls
from .views import *

skill_list = SkillViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

skill_detail = SkillViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

url_list = UrlViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

url_detail = UrlViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    # 로드맵 스킬 전체 조회
    path('skill', skill_list),
    # 로드맵 스킬 단일 조회
    path('skill/<int:pk>', skill_detail),
    # 로드맵 교육영상 전체 조회
    path('url', url_list),
    # 로드맵 교육영상 단일 조회
    path('url/<int:pk>', url_detail),
    # 로드맵 트리구조로 조회 API
    path('tree', views.get_fields),
    # 로드맵 분야별 조회
    path('tree/<field>', views.get_dict),
    # 사용자 현재 레벨 조회 API
    path('level', views.update_level)
    # path('add/', views.add_roadmap)

]
