from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import ProductCategoryAdminForm
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin
from products.models import ProductCategory
from django.db import connection


class CategoryCreateView(CreateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    success_url = reverse_lazy('admins:admin_categories')
    form_class = ProductCategoryAdminForm
    title = 'Админка | Создание категории'


class CategoryListView(ListView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    title = 'Админка | Список категорий'


class CategoryUpdateView(UpdateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = ProductCategoryAdminForm
    title = 'Админка | Обновление категории'
    success_url = reverse_lazy('admins:admin_categories')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set. \
                    update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = ProductCategory
    success_url = reverse_lazy('admins:admin_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
