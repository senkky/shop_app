from rest_framework import serializers

from .models import Product, Order


class ProductSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "created_at",
            "archived",
            "preview",
        )


class OrderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "delivery_address",
            "promocode",
            "created_at",
            "user",
            "products",
            "receipt",
        )
