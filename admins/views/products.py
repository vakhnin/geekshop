from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import ProductAdminForm
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin
from products.models import Product


# Create your views here.
class ProductCreateView(CreateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    success_url = reverse_lazy('admins:admin_products')
    form_class = ProductAdminForm
    title = 'Админка | Создание продукта'


class ProductListView(ListView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    title = 'Админка | Список продуктов'


class ProductUpdateView(UpdateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductAdminForm
    title = 'Админка | Обновление продукта'
    success_url = reverse_lazy('admins:admin_products')


class ProductDeleteView(DeleteView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Product
    success_url = reverse_lazy('admins:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
