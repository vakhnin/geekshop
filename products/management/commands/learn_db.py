from django.core.management.base import BaseCommand
from django.db.models import Q

from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(
            Q(category__name='Обувь') | Q(id=9)
        )
        print(products)

        products = Product.objects.filter(
            Q(category__name='Новинки') | Q(category__name='Обувь')
        )
        print(products)

        products = Product.objects.filter(
            (Q(category__name='Одежда') | Q(category__name='Обувь')) & ~Q(id=9)
        )
        print(products)


