from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

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
    template_name = 'admins/admin-orders-update.html'
    form_class = OrderUpdateForm
    title = 'Админка | Обновление статуса заказа'
    success_url = reverse_lazy('admins:admin_orders')


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
