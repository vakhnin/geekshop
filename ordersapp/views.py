from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView

from baskets.models import Basket
from geekshop import settings
from ordersapp.models import Order, OrderItem
from products.mixin import AddTitleAndNavActiveToContextMixin
from products.models import Product


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class OrderList(ListView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Order
    title = 'GeekShop | Список заказов'
    nav_active = 'user'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


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


class OrderRead(DetailView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Order
    title = 'GeekShop | Просмотр заказа'
    nav_active = 'user'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'


class OrderDelete(DeleteView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Удаление заказа'
    nav_active = 'user'

    login_url = '/auth/login-required'
    redirect_field_name = 'redirect_to'


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
