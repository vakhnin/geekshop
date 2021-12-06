from django.urls import path

import products.views as products

app_name = 'products'

urlpatterns = [
    path('', products.products, name='index'),
    path('category/<int:id_category>/', products.products, name='category'),
    path('page/<int:page>', products.products, name='page'),
    path('product/<int:pk>/', products.product, name='product'),
]
