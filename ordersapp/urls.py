from django.urls import path

from ordersapp.views import OrderList, OrderRead, OrderDelete, order_forming_complete, \
    get_product_data, order_create

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', order_create, name='create'),
    path('read/<int:pk>/', OrderRead.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),
    path('product/<int:pk>/data/', get_product_data, name='product_data'),
]
