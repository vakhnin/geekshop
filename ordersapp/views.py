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
