from django.urls import path

from .views import items_list, update_prices

app_name = "app_goods"

urlpatterns = [
    path('items/', items_list, name='items_list'),
    path('update_prices/', update_prices, name='update_prices'),
]
