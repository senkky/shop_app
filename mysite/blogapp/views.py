from django.views.generic import ListView
from .models import Article
import logging

logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    logger.info('Запрошена страница со списком записей блогов')
    template_name = "blogapp/article-list.html"
    context_object_name = "articles"
    queryset = (
        Article.objects
        .select_related("author", "category")
        .prefetch_related("tags")
        .defer("content")
    )
