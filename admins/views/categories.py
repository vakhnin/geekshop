from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import ProductCategoryAdminForm
from products.mixin import AddTitleAndNavActiveToContextMixin
from products.models import ProductCategory


class CategoryCreateView(CreateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    success_url = reverse_lazy('admins:admin_categories')
    form_class = ProductCategoryAdminForm
    title = 'Админка | Создание категории'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class CategoryListView(ListView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    title = 'Админка | Список категорий'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name


class CategoryUpdateView(UpdateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = ProductCategoryAdminForm
    title = 'Админка | Обновление категории'
    success_url = reverse_lazy('admins:admin_categories')

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    no_permission_template_name = 'admins/admin-no-permission.html'

    def get_template_names(self):
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return self.no_permission_template_name

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set. \
                    update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = ProductCategory
    success_url = reverse_lazy('admins:admin_categories')

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
