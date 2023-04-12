from django.urls import path, include

from core import views
urlpatterns = [
    path('', views.index),
    # crawling으로 url 매핑
    path('crawling/', include("crawling.urls")),
    # user로 url 매핑
    path('user/', include('account.urls')),
    # roadmap으로 url 매핑
    path('roadmap/',include('roadmap.urls'))



]
