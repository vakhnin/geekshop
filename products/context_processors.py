from baskets.models import Basket
from geekshop import settings
from products.models import ProductCategory
from django.core.cache import cache


def basket(request):
    baskets_list = []
    if request.user.is_authenticated:
        baskets_list = Basket.objects.filter(user=request.user)

    return {
        'baskets': baskets_list
    }


def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def categories(request):
    categories_list = get_link_category()

    return {'categories': categories_list}
