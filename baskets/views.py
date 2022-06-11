from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, TemplateView

from authapp.models import ShopUser
from baskets.models import Basket
from products.mixin import UserDispatchMixin, BaseClassContextMixin
from products.models import Product


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class BasketView(TemplateView, BaseClassContextMixin, UserDispatchMixin):
    title = 'Geekshop - Корзина'
    template_name = 'baskets/basket-page.html'


@login_required
def basket_add(request, id):
    if is_ajax(request=request):
        user_select = request.user
        product = Product.objects.get(id=id)
        baskets = Basket.objects.filter(user=user_select, product=product)
        if baskets:
            basket = baskets.first()
            basket.quantity = F('quantity') + 1
            basket.save()
        else:
            Basket.objects.create(user=user_select, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id_basket, quantity):
    if is_ajax(request=request):
        basket = Basket.objects.get(id=id_basket)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/basket.html', context)
        return JsonResponse({'result': result})


@login_required
def basket_remove(request, pk):
    Basket.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
