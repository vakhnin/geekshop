from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .mixin import AddTitleAndNavActiveToContextMixin
from .models import Product


# Create your views here.
class IndexTemplateView(TemplateView, AddTitleAndNavActiveToContextMixin):
    title = 'geekshop - Главная'
    nav_active = 'index'
    template_name = 'products/index.html'


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class ProductListView(ListView, AddTitleAndNavActiveToContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'
    nav_active = 'catalog'
    paginate_by = 3
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_category'] = 0
        return context


class CategoryProductListView(ListView, AddTitleAndNavActiveToContextMixin):
    context_object_name = 'products'
    model = Product
    template_name = 'products/products.html'
    title = 'geekshop - Каталог'
    nav_active = 'catalog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_category = self.kwargs['id_category']
        context['id_category'] = id_category
        return context

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
