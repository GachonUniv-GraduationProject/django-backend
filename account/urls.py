from django.urls import path
from .views import *

urlpatterns = [
    path('', UserAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('signup', RegistrationAPIView.as_view()),
    path("profile/<int:user_pk>/update", ProfileDetailAPIView.as_view()),
    path("profile/roadmap", ProfileRoadmapAPIView.as_view()),
    path("profile/roadmap/url", RoadmapGetURLAPIView.as_view()),
    path("profile/capability", ProfileCapabilityAPIView.as_view()),
    path("company/survey", CompanyAPIView.as_view()),
    path("profile/mypage", MyPageAPIView.as_view()),
    path("company/recommendation", CompanyRecommendationAPIView.as_view())

    # path('tech/', views.TechView.as_view(), name="tech")
]
