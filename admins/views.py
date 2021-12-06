# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryAdminForm, ProductAdminForm
from authapp.models import ShopUser
# Create your views here.
from products.mixin import BaseClassContextMixin, CustomDispatchMixin
from products.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


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
@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'admins/admin-products-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductAdminForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_products'))
    else:
        form = ProductAdminForm()
    context = {
        'title': 'Geekshop - Админ | Создание продукта',
        'form': form
    }
    return render(request, 'admins/admin-products-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_update(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductAdminForm(data=request.POST, instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_products'))
    else:
        form = ProductAdminForm(instance=product)
    context = {
        'title': 'Geekshop - Админ | Обновление продукта',
        'form': form,
        'product': product
    }
    return render(request, 'admins/admin-products-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_delete(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        product.is_active = False
        product.save()

    return HttpResponseRedirect(reverse('admins:admin_products'))
