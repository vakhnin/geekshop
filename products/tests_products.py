from django.test import TestCase
from products.models import Product, ProductCategory


class ProductsTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(name="обувь")

        self.product_1 = Product.objects.create(name="ботинки 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)
        self.product_2 = Product.objects.create(name="ботинки 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)
        self.product_3 = Product.objects.create(name="ботинки 3",
                                                category=category,
                                                price=998.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="ботинки 1")
        product_2 = Product.objects.get(name="ботинки 2")

        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="ботинки 1")
        product_2 = Product.objects.get(name="ботинки 2")
        self.assertEqual(str(product_1), 'ботинки 1 (обувь)')
        self.assertEqual(str(product_2), 'ботинки 2 (обувь)')
