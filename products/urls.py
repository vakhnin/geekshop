from django.urls import path

import products.views as products

app_name = 'products'

urlpatterns = [
    path('', products.ProductListView.as_view(), name='index'),
    path('category/<int:id_category>/', products.products, name='category'),
    path('page/<int:page>', products.ProductListView.as_view(), name='page'),
    path('product/<int:pk>/', products.ProductDetailView.as_view(), name='product'),
]
