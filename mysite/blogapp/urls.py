from django.urls import path, include

from .views import ArticleListView

app_name = "blogapp"

urlpatterns = [
    path('Article/', ArticleListView.as_view(), name="article-list"),
]
