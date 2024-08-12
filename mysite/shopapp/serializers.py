from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "prices",
            "discount",
            "created_at",
            "archived",
            "preview",
        )