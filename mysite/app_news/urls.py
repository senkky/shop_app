from django.urls import path

from .views import get_news_in_custom_format, NewsItemDetailView

app_name = "app_news"

urlpatterns = [
    path('', get_news_in_custom_format, name="news_list"),
    path('<int:pk>/', NewsItemDetailView.as_view(), name="news-item"),
]
