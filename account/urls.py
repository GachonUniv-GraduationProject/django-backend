from django.urls import path
from .views import *
# /user
urlpatterns = [
    # get user info
    path('', UserAPI.as_view()),
    # login api
    path('login', LoginAPI.as_view()),
    # signup api
    path('signup', RegistrationAPIView.as_view()),
    # user profile update api
    path("profile/<int:user_pk>/update", ProfileDetailAPIView.as_view()),
    # get user roadmap api
    path("profile/roadmap", ProfileRoadmapAPIView.as_view()),
    # get user roadmap education information api
    path("profile/roadmap/url", RoadmapGetURLAPIView.as_view()),
    # get user capability api
    path("profile/capability", ProfileCapabilityAPIView.as_view()),
    # company survey api
    path("company/survey", CompanyAPIView.as_view()),
    # mypage info api
    path("profile/mypage", MyPageAPIView.as_view()),
    # company get tech api
    path("company/recommendation", CompanyRecommendationAPIView.as_view())

    # path('tech/', views.TechView.as_view(), name="tech")
]
