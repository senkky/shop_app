from django.urls import path
from .views import (
    BlogsListView,
    logout_view,
    BlogCreateView,
    AboutMeView,
    UserUpdateView,
    RegisterUserView,
    LoginUserView,
    # profile,
)

app_name = "blog_app"

urlpatterns = [
    path("index/", BlogsListView.as_view(), name="index"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("index/<int:pk>/blog_creat/", BlogCreateView.as_view(), name="create_blog"),
    path("index/<int:pk>/", AboutMeView.as_view(), name="about-me"),
    path("index/<int:pk>/update/", UserUpdateView.as_view(), name="profile_update_form"),
]
