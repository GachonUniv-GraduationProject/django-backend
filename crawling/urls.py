from django.urls import path
from crawling import views
from .views import *

# get list
data_list = DataViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

data_detail = DataViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

keyword_list = KeywordViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

keyword_detail = KeywordViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})



urlpatterns = [
    # get data api
    path('data', data_list),
    # get single data api
    path('data/<int:pk>', data_detail),
    # get keyword list api
    path('keyword', keyword_list),
    # get single keyword api
    path('keyword/<int:pk>', keyword_detail),
    # get trend field api
    path('trend', views.get_field),
    # get trend per field api
    path('trend/<field>', views.get_trend_new),
    # update trend api
    path('trend_update', views.trend_update),
    # update keyword api
    path('keyword/update', views.keyword_update),
    # update roadmap api
    path('update', views.recruit_json)

]
