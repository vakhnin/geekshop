from django.views.generic import DetailView, ListView, TemplateView

from .mixin import BaseClassContextMixin
from .models import Product


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


class ProductDetailView(DetailView, BaseClassContextMixin):
    context_object_name = 'product'
    model = Product
    template_name = 'products/product.html'
    title = 'geekshop - Детальная информация'
