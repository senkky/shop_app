from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse
from .models import Housing, News


class LatestNewsFeed(Feed):
    title = "Новости"
    link = "/sitenews/"
    description = "Самые свежие новости."

    def items(self) -> QuerySet:
        return News.objects.order_by('published')

    def item_title(self, item: News) -> str:
        return item.heading

    def item_description(self, item: News) -> str:
        return item.text

    def item_link(self, item: News) -> str:
        return reverse('app_house:news', args=[item.pk])

    class LatestHouseFeed(Feed):
        title = "Жильё"
        link = "/sitehouse/"
        description = "Дома, квартиры, дачи."

        def items(self) -> QuerySet:
            return News.objects.order_by('published')

        def item_title(self, item: Housing) -> str:
            return item.address

        def item_description(self, item: Housing) -> str:
            return item.total_area

        def item_link(self, item: Housing) -> str:
            return reverse('app_house:house', args=[item.pk])
