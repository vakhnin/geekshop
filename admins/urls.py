from django.urls import path

from admins.views import index, admin_users_create, admin_users_update, admin_users_delete, admin_users, \
    admin_products, \
    admin_products_create, admin_products_update, admin_products_delete, CategoryListView, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView

app_name = 'admins'
urlpatterns = [

    path('', index, name='index'),

    path('users/', admin_users, name='admin_users'),
    path('users-create/', admin_users_create, name='admin_users_create'),
    path('users-update/<int:pk>', admin_users_update, name='admin_users_update'),
    path('users-delete/<int:pk>', admin_users_delete, name='admin_users_delete'),

    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('categories-create/', CategoryCreateView.as_view(), name='admin_categories_create'),
    path('categories-update/<int:pk>', CategoryUpdateView.as_view(), name='admin_categories_update'),
    path('categories-delete/<int:pk>', CategoryDeleteView.as_view(), name='admin_categories_delete'),

    path('products/', admin_products, name='admin_products'),
    path('products-create/', admin_products_create, name='admin_products_create'),
    path('products-update/<int:pk>', admin_products_update, name='admin_products_update'),
    path('products-delete/<int:pk>', admin_products_delete, name='admin_products_delete'),
]
