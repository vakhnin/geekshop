from django.urls import path

import products.views as products

app_name = 'products'

urlpatterns = [
   path('', products.products, name='index'),
   path('<int:id>/', products.products, name='category'),
   path('product/<int:id>/', products.product, name='product'),
]
