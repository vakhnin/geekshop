from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from baskets.models import Basket
from products.mixin import UserIsLoginMixin, AddTitleToContextMixin
from products.models import Product


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class BasketView(TemplateView, AddTitleToContextMixin, UserIsLoginMixin):
    title = 'Geekshop - Корзина'
    template_name = 'baskets/basket.html'


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
        result = render_to_string('baskets/includes/inc_basket.html', context)
        return JsonResponse({'result': result})


@login_required
def basket_remove(request, pk):
    Basket.objects.get(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
