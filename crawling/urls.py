from django.urls import path
from crawling import views
from .views import DataViewSet, KeywordViewSet

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
    # get으로 크롤링 데이터 가져올 수 있게, 파라미터로 특정 크롤링 결과만 가져올 수 잇게하자
    # post면 크롤링 데이터 추가할 수 있게,
    # url도 recruit이 아니라, root url로 변경하자
    path('data', data_list),
    path('data/<int:pk>', data_detail),
    path('keyword', keyword_list),
    path('keyword/<int:pk>', keyword_detail),
    path('trend', views.get_field),
    path('trend/<field>', views.get_trend),
    path('trend_update', views.trend_update),
    path('keyword/update', views.keyword_update),
    path('update', views.recruit_json)

]
