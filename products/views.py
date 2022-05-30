from django.views.generic import DetailView, ListView, TemplateView

from geekshop import settings
from .mixin import BaseClassContextMixin
from .models import Product

from django.core.cache import cache


# Create your views here.
class IndexTemplateView(TemplateView, BaseClassContextMixin):
    title = 'geekshop - Главная'
    template_name = 'products/index.html'


class ProductListView(ListView, BaseClassContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'
    paginate_by = 3


class CategoryProductListView(ListView, BaseClassContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'

    def get_queryset(self):
        return Product.objects. \
                   filter(category=self.kwargs['id_category'], is_active=True,
                          category__is_active=True). \
                   select_related('category')[:3]


def get_product_(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


class ProductDetailView(DetailView, BaseClassContextMixin):
    context_object_name = 'product'
    model = Product
    template_name = 'products/product.html'
    title = 'geekshop - Детальная информация'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['product'] = get_product_(self.kwargs.get('pk'))
        return context
