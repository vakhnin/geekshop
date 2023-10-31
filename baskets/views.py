from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from baskets.models import Basket
from products.mixin import AddTitleAndNavActiveToContextMixin
from products.models import Product

INCREASE_PRODUCT_ACTION = 'increase-count'
DECREASE_PRODUCT_ACTION = 'decrease-count'


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class BasketView(TemplateView, LoginRequiredMixin, AddTitleAndNavActiveToContextMixin):
    title = 'Geekshop - Корзина'
    nav_active = 'basket'
    template_name = 'baskets/basket.html'

    login_url = "/auth/login-required"
    redirect_field_name = "redirect_to"


@login_required
def basket_add(request, id):
    if is_ajax(request=request):
        user_select = request.user
        product = Product.objects.get(id=id)

        if product.quantity > 0:
            baskets = Basket.objects.filter(user=user_select, product=product)
            if baskets:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
            else:
                Basket.objects.create(user=user_select, product=product, quantity=1)

        baskets = Basket.objects.filter(user=request.user)
        total_quantity = 0
        for bask in baskets:
            total_quantity += bask.quantity
        return JsonResponse({'no_product': product.quantity <= 0,
                             'total_quantity': total_quantity})


@login_required
def basket_edit(request, id_basket, action):
    if is_ajax(request=request):
        no_product = False
        basket = Basket.objects.get(id=id_basket)
        product = Product.objects.get(id=basket.product.id)

        if action == DECREASE_PRODUCT_ACTION and basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        elif action == INCREASE_PRODUCT_ACTION:
            if product.quantity > 0:
                basket.quantity += 1
                basket.save()
            else:
                no_product = True

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/includes/inc_basket.html', context)
        return JsonResponse({'no_product': no_product,
                             'result': result})


@login_required
def basket_remove(request, pk):
    Basket.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
