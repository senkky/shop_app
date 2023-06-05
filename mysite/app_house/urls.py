from django.urls import path

from .views import NewsDetailView, HouseDetailView

app_name = "app_house"

urlpatterns = [
    path('<int:pk>/', NewsDetailView.as_view(), name="news"),
    path('<int:pk>/', HouseDetailView.as_view(), name="house"),
]
