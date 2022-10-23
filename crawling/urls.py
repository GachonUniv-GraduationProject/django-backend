from django.urls import path
from crawling import views

urlpatterns = [
    # get으로 크롤링 데이터 가져올 수 있게, 파라미터로 특정 크롤링 결과만 가져올 수 잇게하자
    # post면 크롤링 데이터 추가할 수 있게,
    # url도 recruit이 아니라, root url로 변경하자
    path('recruit/', views.recruit_json)
]