from django.urls import path
from crawling import views
from .views import *

# 목록 보여주기
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
    # 데이터 조회용 API
    path('data', data_list),
    # 싱글 데이터 조회 API
    path('data/<int:pk>', data_detail),
    # 키워드 리스트 조회 API
    path('keyword', keyword_list),
    # 싱글 키워드 조회 API
    path('keyword/<int:pk>', keyword_detail),
    # 트렌드 분야 조회 API
    path('trend', views.get_field),
    # 트렌드 분야별 조회 API
    path('trend/<field>', views.get_trend_new),
    # 트렌드 업데이트 API
    path('trend_update', views.trend_update),
    # 키워드 업데이트 API
    path('keyword/update', views.keyword_update),
    # 로드맵 업데이트 API
    path('update', views.recruit_json)

]
