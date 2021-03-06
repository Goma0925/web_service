from django.urls import path
from applications.users import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    #path("login/?next=/<str:next_path>/", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    #path("mypage/", views.get_mypage, name="mypage"),
    path("mypage/joinlist/", views.retrieve_my_joinlist, name="retrieve_my_joinlist"),
    path("mypage/myhostinglist/", views.retrieve_my_hostinglist, name="retrieve_my_hostinglist"),
    path("mypage/mywatchlist/", views.retrieve_my_watchlist, name="retrieve_my_watchlist"),
    path("mypage/editprofile/", views.edit_profile, name="edit_profile"),
    path("mypage/profile/", views.retrieve_profile, name="retrieve_profile"),
    path("mypage/photos/", views.edit_my_images, name="edit_my_images")
]
