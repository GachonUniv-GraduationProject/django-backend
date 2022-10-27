from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    # 회원가입, 로그인을 관리
    # 회원가입은 signup으로 post 요청이 오면 처리해줄것임
    # 로그인도 login으로 post 요청, 로그아웃은 logout으로 post 요청오게끔
    # 기술 스택은 tech, get으로 오면 유저의 기술 스택 가져오기, post면 추가하기, patch면 수정, delete으로 삭제되게
    # path('signup/', views.UserCreate.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    # path('check/', views.check_users),
    # path('logintest/', views.login_test),
    # path('signuptest/', views.signup_test),
    # path('addtech/', views.add_tech_stack),
    # path('', views.user_check),
    # path('logout/', views.logout)
    path('', views.IndexView.as_view(), name="index"),
    path('login/',views.LoginView.as_view(), name="login"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('tech/', views.TechView.as_view(), name="tech")
 ]
