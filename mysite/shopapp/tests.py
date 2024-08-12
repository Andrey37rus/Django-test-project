from string import ascii_letters
from django.urls import reverse
from django.test import TestCase
from random import choices

from shopapp.models import Product


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
                "discount": "10",
            }
        )

        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )