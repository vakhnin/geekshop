from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from admins.forms import OrderUpdateForm
from ordersapp.models import Order
from products.mixin import AddTitleToContextMixin, UserIsSuperuserMixin
from products.models import ProductCategory
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


# Create your views here.
class OrdertListView(ListView, AddTitleToContextMixin, UserIsSuperuserMixin):
    model = Order
    template_name = 'admins/admin-orders-read.html'
    title = 'Админка | Список заказов'


class OrderUpdateView(UpdateView, AddTitleToContextMixin, UserIsSuperuserMixin):
    model = Order
    template_name = 'admins/admin-orders-update-delete.html'
    form_class = OrderUpdateForm
    title = 'Админка | Обновление статуса заказа'
    success_url = reverse_lazy('admins:admin_orders')


class OrderDeleteView(DeleteView, AddTitleToContextMixin, UserIsSuperuserMixin):
    model = Order
    success_url = reverse_lazy('admins:admin_orders')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        self.redirect = HttpResponseRedirect(self.get_success_url())
        return self.redirect


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
