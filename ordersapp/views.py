from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from geekshop import settings
from products.mixin import AddTitleToContextMixin, UserIsLoginMixin
from baskets.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem
from products.models import Product


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class OrderList(ListView, AddTitleToContextMixin, UserIsLoginMixin):
    model = Order
    title = 'GeekShop | Список заказов'


class OrderCreate(CreateView, AddTitleToContextMixin, UserIsLoginMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_item.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                basket_item.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderCreate, self).form_valid(form)


@login_required
def order_create(request):
    with transaction.atomic():
        user_select = request.user

        order = Order(user=user_select)
        order.save()

        baskets = Basket.objects.filter(user=user_select)
        for basket in baskets:
            order_item = OrderItem(order=order, product=basket.product, quantity=basket.quantity)
            order_item.save()
            basket.delete()
    return HttpResponseRedirect(reverse('orders:list'))


class OrderUpdate(UpdateView, AddTitleToContextMixin, UserIsLoginMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Создание заказа'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:

            formset = OrderFormSet(instance=self.object)
            for num, form in enumerate(formset.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

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
        return super(OrderUpdate, self).form_valid(form)


class OrderRead(DetailView, AddTitleToContextMixin, UserIsLoginMixin):
    model = Order
    title = 'GeekShop | Просмотр заказа'


class OrderDelete(DeleteView, AddTitleToContextMixin, UserIsLoginMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Удаление заказа'


def order_forming_complete(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.SEND_TO_PROCESSED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


def get_product_data(request, pk):
    if is_ajax(request=request):
        product = Product.objects.get(pk=pk)
        if product:
            image = settings.MEDIA_URL + str(product.image)
            return JsonResponse({
                'price': product.price,
                'image': image,
            })
        return JsonResponse({'price': 0, 'image': ''})
