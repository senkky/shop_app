from django import forms

from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products", "promocode", "delivery_address"