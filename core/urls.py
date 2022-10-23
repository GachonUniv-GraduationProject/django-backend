from django.urls import path, include

from core import views
urlpatterns = [
    path('', views.index),
    # 크롤링, 유저, 로드맵에 url을 매핑해준다.
    path('crawling/', include("crawling.urls")),
    path('user/', include('account.urls')),
    path('roadmap/',include('roadmap.urls'))



]
