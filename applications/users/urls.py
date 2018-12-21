from django.urls import path
from applications.users import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    #path("login/?next=/<str:next_path>/", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("mypage/", views.mypage, name="mypage"),
]
