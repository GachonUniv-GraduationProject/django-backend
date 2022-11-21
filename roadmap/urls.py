from django.urls import path, include
from . import views
from rest_framework import urls
from .views import SkillViewSet,UrlViewSet

skill_list = SkillViewSet.as_view({
    'get':'list',
    'post':'create'
})

skill_detail = SkillViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})

url_list = UrlViewSet.as_view({
    'get':'list',
    'post':'create'
})

url_detail = UrlViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})



urlpatterns = [
    # 로드맵 추가도 post로하고, 조회는 get으로,
    # 경로도 root 경로로 변경하자
    path('skill',skill_list),
    path('skill/<int:pk>',skill_detail),
    path('url',url_list),
    path('url/<int:pk>',url_detail)
    # path('add/', views.add_roadmap)

]
