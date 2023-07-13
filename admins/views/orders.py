from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from admins.forms import OrderUpdateForm, OrderCreateForm
from admins.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem
from products.mixin import AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin
from products.models import ProductCategory
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection, transaction


# Create your views here.
class OrderListView(ListView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Order
    template_name = 'admins/admin-orders-read.html'
    title = 'Админка | Список заказов'


class OrderCreateView(CreateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Order
    form_class = OrderCreateForm
    template_name = 'admins/admin-orders-create.html'
    success_url = reverse_lazy('admins:admin_orders')
    title = 'Админка | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            context['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            context['orderitems'] = OrderFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        return super().form_valid(form)


class OrderUpdateView(UpdateView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
    model = Order
    template_name = 'admins/admin-orders-update-delete.html'
    form_class = OrderUpdateForm
    title = 'Админка | Редактирование заказа'
    success_url = reverse_lazy('admins:admin_orders')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=0)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for num, form in enumerate(formset.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['image'] = form.instance.product.image

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

            form.save()
        return super().form_valid(form)


class OrderDeleteView(DeleteView, AddTitleAndNavActiveToContextMixin, UserIsSuperuserMixin):
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
