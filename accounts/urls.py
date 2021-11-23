from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# 커스텀 로그인,회원가입 이용위함

app_name = 'accounts'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
