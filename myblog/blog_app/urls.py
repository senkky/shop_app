from django.urls import path
from .views import (
    BlogsListView,
    logout_view,
    AboutMeView,
    UserUpdateView,
    RegisterUserView,
    LoginUserView,
    create_to_blog,
    UserListView,
    UserDetailView,
)

app_name = "blog_app"

urlpatterns = [
    path("index/", BlogsListView.as_view(), name="index"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("index/<int:pk>/blog_creat/", create_to_blog, name="create_blog"),
    path("index/about/", AboutMeView.as_view(), name="about-me"),
    path("index/<int:pk>/user_details/", UserDetailView.as_view(), name="user_details"),
    path("index/<int:pk>/update/", UserUpdateView.as_view(), name="profile_update_form"),
]
