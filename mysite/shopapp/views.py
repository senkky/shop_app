"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from timeit import default_timer
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
import logging

from .forms import ProductForm, OrdersForm, GroupForm
from .mixins import LogoutIfNotStaffMixin
from .models import Product, Order, ProductImage
from django.views import View
from .serializers import ProductSerialiser, OrderSerialiser

logger = logging.getLogger(__name__)


@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerialiser
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product by ID",
        description="Retrieves **product**, returns 404 if not found",
        responses={
            200: ProductSerialiser,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerialiser
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["user", "products"]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "created_at",
        "user",
        "products",
    ]
    ordering_fields = [
        "created_at",
        "user",
        "delivery_address",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999)
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/product_details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"

    # def get(self, request: HttpRequest, pk: int) -> HttpResponse:
    #     product = get_object_or_404(Product, pk=pk)
    #     context = {
    #         "product": product,
    #     }
    #     return render(request, 'shopapp/products-details.html', context=context)


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

    # def get_queryset(self):
    #     product = self.request.product  # TODO интересно, что это за товар?
    #     product_list_cache_key = 'product_list: {}'.format(product)
    #     # TODO Как видите, тут выполнено только сохранение данные в кэше, а использования данных из кэша нет.
    #     #  Правда в лекции это не показано подробно, но смысл такой: первым делом смотрим в кеше наличие данных по ключу
    #     #  с помощью cache.get, если в кэше нужных ключей нет, только тогда делаем запросы в базу и сохраняем в кеше
    #     #  с помощью cache.set "добытую" информацию. При использовании get_or_set процесс упрощается с двух шагов до одного
    #     cache.get_or_set(product_list_cache_key, product, 30 * 60)  # TODO вместо product надо сделать запрос в базу,
    #                                                                 #  кроме, надо присвоить результат функции перерменной...
    #     return product.objects.filter(archived=False)  # TODO ...а тут указать эту переменную


# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        return self.request.user.is_superuser

    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             # name = form.cleaned_data["name"]
#             # price = form.cleaned_data["price"]
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "shopapp/create-product.html", context=context)


class ProductUpdateView(UpdateView):
    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(product=self.object, image=image)
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#     }
#     return render(request, 'shopapp/orders-list.html', context=context)


class OrderDetailView(PermissionRequiredMixin, DetailView):
    # permission_required = "view_order"
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "user", "products", "promocode", "delivery_address"
    success_url = reverse_lazy("shopapp:order_list")
    logger.info(f'Создан заказ {fields}')


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = OrdersForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("shopapp:order_list")
#             return redirect(url)
#     else:
#         form = OrdersForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "shopapp/create-order.html", context=context)


class OrderUpdateView(UpdateView):
    model = Order
    fields = "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class OrderDataExportView(PermissionRequiredMixin, LogoutIfNotStaffMixin, View):
    permission_required = 'is_staff'

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
            {
                "user": order.user.pk,
                "products": order.products.pk,
                "pk": order.pk,
                "promocode": order.promocode,
                "delivery_address": order.delivery_address,
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})
