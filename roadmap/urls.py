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
    # get roadmap skill list
    path('skill', skill_list),
    # get single roadmap skill
    path('skill/<int:pk>', skill_detail),
    # get roadmap education video list
    path('url', url_list),
    # get single roadmap view
    path('url/<int:pk>', url_detail),
    # get roadmap tree
    path('tree', views.get_fields),
    # get roadmap field
    path('tree/<field>', views.get_dict),
    # get user current level
    path('level', views.update_level)
    # path('add/', views.add_roadmap)

]
