from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import ProductAdminForm
from products.mixin import AddTitleAndNavActiveToContextMixin
from products.models import Product


# Create your views here.
class ProductCreateView(CreateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    success_url = reverse_lazy('admins:admin_products')
    form_class = ProductAdminForm
    title = 'Админка | Создание продукта'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class ProductListView(ListView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    title = 'Админка | Список продуктов'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class ProductUpdateView(UpdateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductAdminForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('admins:admin_products')

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class ProductDeleteView(DeleteView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Product
    success_url = reverse_lazy('admins:admin_products')

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
