from django.views.generic import DetailView

from .models import News, Housing


class NewsDetailView(DetailView):
    model = News
    template_name = 'app_house/news_detail.html'


class HouseDetailView(DetailView):
    model = Housing
    template_name = 'app_house/house_detail.html'
