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


# users CRUD
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'admins/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'users': ShopUser.objects.all()
    }
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminRegisterForm()
    context = {
        'title': 'Geekshop - Админ | Регистрация',
        'form': form
    }
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, pk):
    user_select = ShopUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admin_users'))
    else:
        form = UserAdminProfileForm(instance=user_select)
    context = {
        'title': 'Geekshop - Админ | Обновление',
        'form': form,
        'user_select': user_select
    }
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, pk):
    if request.method == 'POST':
        user = ShopUser.objects.get(pk=pk)
        user.is_active = False
        user.save()

    return HttpResponseRedirect(reverse('admins:admin_users'))


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
