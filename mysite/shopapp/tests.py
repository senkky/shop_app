from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from shopapp.utils import add_two_numbers
from .models import Product, Order


class AddTwoNumberTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10"
            },
            HTTP_USER_AGENT="Mozilla/5.0",
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    # def tearDown(self) -> None:
    #     self.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestView(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"),
                                   HTTP_USER_AGENT="Mozilla/5.0",
                                   )
        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)
        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:order_list"), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:order_list"), HTTP_USER_AGENT="Mozilla/5.0")
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
            HTTP_USER_AGENT="Mozilla/5.0",
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrderDetailsViewTestCase(TestCase):
    fixtures = [
        'order-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)
        cls.order = (
            Order.objects
            .select_related("user")
            .prefetch_related("products")
        )

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order.create(delivery_address="SALE123", promocode="SALE123")

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk}),
            HTTP_USER_AGENT="Mozilla/5.0"
        )
        orders = Order.objects.all()
        orders_data = response.json()
        expected_data = [
            {
                "user": self.user.pk,
                "pk": order.pk,
                "promocode": order.promocode,
                "delivery_address": order.delivery_address,

            }
            for order in orders
        ]
        print(expected_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            orders_data["order"],
            expected_data,
        )


class OrderExportViewTestCase(TestCase):
    fixtures = [
        'order-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob_test", password="qwerty", is_staff=True)
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:order-export"),
            HTTP_USER_AGENT="Mozilla/5.0",
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "user": self.user.pk,
                "products": order.products.pk,
                "pk": order.pk,
                "promocode": order.promocode,
                "delivery_address": order.delivery_address,
            }
            for order in orders
        ]
        order_data = response.json()
        self.assertEqual(
            order_data["order"],
            expected_data,
        )
