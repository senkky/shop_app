from django.contrib.sitemaps import Sitemap
from app_house.models import News, Housing


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return News.objects.all()


class HousingSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Housing.objects.all()
