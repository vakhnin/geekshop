from django.http import HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import render_to_string

from baskets.models import Basket
from products.models import Product


def basket_add(request, id):
    if request.is_ajax():
        user_select = request.user
        product = Product.objects.get(id=id)
        baskets = Basket.objects.filter(user=user_select, product=product)
        if baskets:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(user=user_select, product=product, quantity=1)

        products = Product.objects.all()
        context = {'products': products}
        result = render_to_string('mainapp/includes/card.html', context)
        return JsonResponse({'result': result})


def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
