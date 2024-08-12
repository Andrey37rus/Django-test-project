from typing import Sequence

from django.core.management import BaseCommand

from shopapp.models import Order, Product

from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains="smartphone"
        ).update(discount=10)

        print(result)


        # info = [
        #     ('smartphone 1', 199),
        #     ('smartphone 2', 299),
        #     ('smartphone 3', 399),
        # ]
        #
        # products = [
        #     Product(name=name, prices=prices)
        #     for name, prices in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write("Done")
