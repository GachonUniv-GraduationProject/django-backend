from django.urls import path
from .views import *
# /user
urlpatterns = [
    # 유저 정보 조회 API
    path('', UserAPI.as_view()),
    # 로그인 API
    path('login', LoginAPI.as_view()),
    # 회원가입 API
    path('signup', RegistrationAPIView.as_view()),
    # 유저 프로필 업데이트 API
    path("profile/<int:user_pk>/update", ProfileDetailAPIView.as_view()),
    # 유저로드맵 조회 API
    path("profile/roadmap", ProfileRoadmapAPIView.as_view()),
    # 유저 로드맵 교육 자료 조회 API
    path("profile/roadmap/url", RoadmapGetURLAPIView.as_view()),
    # 유저 capability 조회 API
    path("profile/capability", ProfileCapabilityAPIView.as_view()),
    # 기업 설문용 API
    path("company/survey", CompanyAPIView.as_view()),
    # 마이페이지 조회용 API
    path("profile/mypage", MyPageAPIView.as_view()),
    # 기업 추천 API
    path("company/recommendation", CompanyRecommendationAPIView.as_view())

    # path('tech/', views.TechView.as_view(), name="tech")
]
