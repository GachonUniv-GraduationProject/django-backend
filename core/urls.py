from django.urls import path, include

from core import views
urlpatterns = [
    path('', views.index),
    path('crawling/', include("crawling.urls")),
    path('user/', include('account.urls')),




]
