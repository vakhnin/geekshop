# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryAdminForm, ProductAdminForm
from authapp.models import ShopUser
# Create your views here.
from products.mixin import BaseClassContextMixin, CustomDispatchMixin
from products.models import ProductCategory, Product


class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    template_name = 'admins/admin.html'
    title = 'Админка'


# users CRUD
class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Создать пользователя'


class UserListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'admins/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Обновить пользователя'


class UserDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
    model = ShopUser
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    title = 'Админка | Удалить пользователя'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# categories CRUD
class CategoryCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    success_url = reverse_lazy('admins:admin_categories')
    form_class = ProductCategoryAdminForm
    title = 'Админка | Создание категории'


class CategoryListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    title = 'Админка | Список категорий'


class CategoryUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = ProductCategoryAdminForm
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('admins:admin_categories')


class CategoryDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategory
    success_url = reverse_lazy('admins:admin_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# products CRUD
class ProductCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    success_url = reverse_lazy('admins:admin_products')
    form_class = ProductAdminForm
    title = 'Админка | Создание продукта'


class ProductListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    title = 'Админка | Список продуктов'


class ProductUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductAdminForm
    title = 'Админка | Обновления категории'
    success_url = reverse_lazy('admins:admin_products')


class ProductDeleteView(DeleteView, BaseClassContextMixin, CustomDispatchMixin):
    model = Product
    success_url = reverse_lazy('admins:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
