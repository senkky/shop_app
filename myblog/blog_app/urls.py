from django.urls import path
from .views import (
    BlogsListView,
    logout_view,
    BlogCreateView,
    AboutMeView,
    UserUpdateView,
    RegisterUser,
    LoginUserView,
)

app_name = "blog_app"

urlpatterns = [
    path("index/", BlogsListView.as_view(), name="index"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("index/blog_creat/<int:pk>/", BlogCreateView.as_view(), name="create_blog"),
    path("index/<int:pk>/", AboutMeView.as_view(), name="about-me"),
    path("index/update/<int:pk>/", UserUpdateView.as_view(), name="profile_update_form"),
]
