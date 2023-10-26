import json
import os

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from products.models import ProductCategory, Product

JSON_PATH = 'products' + os.sep + 'fixtures'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] = _category
            new_category = Product(**prod)
            new_category.save()

        # Создаем суперпользователя при помощи менеджера модели
        if not ShopUser.objects.filter(username='admin'):
            ShopUser.objects.create_superuser(username='admin',
                                              email='admin@admin.local',
                                              password='admin',
                                              age=33)
