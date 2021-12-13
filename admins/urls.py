from django.urls import path

from admins.views import CategoryListView, \
    CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, IndexTemplateView

app_name = 'admins'
urlpatterns = [

    path('', IndexTemplateView.as_view(), name='index'),

    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),

    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('categories-create/', CategoryCreateView.as_view(), name='admin_categories_create'),
    path('categories-update/<int:pk>', CategoryUpdateView.as_view(), name='admin_categories_update'),
    path('categories-delete/<int:pk>', CategoryDeleteView.as_view(), name='admin_categories_delete'),

    path('products/', ProductListView.as_view(), name='admin_products'),
    path('products-create/', ProductCreateView.as_view(), name='admin_products_create'),
    path('products-update/<int:pk>', ProductUpdateView.as_view(), name='admin_products_update'),
    path('products-delete/<int:pk>', ProductDeleteView.as_view(), name='admin_products_delete'),
]
