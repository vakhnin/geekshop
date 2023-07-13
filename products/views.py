from django.views.generic import DetailView, ListView, TemplateView

from .mixin import AddTitleAndNavActiveToContextMixin
from .models import Product


# Create your views here.
class IndexTemplateView(TemplateView, AddTitleAndNavActiveToContextMixin):
    title = 'geekshop - Главная'
    nav_active = 'index'
    template_name = 'products/index.html'


class ProductListView(ListView, AddTitleAndNavActiveToContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'
    nav_active = 'catalog'
    paginate_by = 3
    ordering = ['-id']


class CategoryProductListView(ListView, AddTitleAndNavActiveToContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'
    nav_active = 'catalog'

    def get_queryset(self):
        return Product.objects. \
                   filter(category=self.kwargs['id_category'], is_active=True,
                          category__is_active=True). \
                   select_related('category')[:3]


class ProductDetailView(DetailView, AddTitleAndNavActiveToContextMixin):
    context_object_name = 'product'
    model = Product
    template_name = 'products/product.html'
    title = 'geekshop - Детальная информация'
    nav_active = 'catalog'
