from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView

from .mixin import BaseClassContextMixin
from .models import Product, ProductCategory


# Create your views here.
def main(request):
    title = "geekshop - Главная"
    content = {'title': title}

    return render(request, 'products/index.html', content)


def products(request, id_category=None, page=1):
    title = 'geekshop - Каталог'

    if id_category:
        products = Product.objects.filter(category_id=id_category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    products = products_paginator
    categories = ProductCategory.objects.all()
    context = {
        'title': title,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/products.html', context)


class ProductDetailView(DetailView, BaseClassContextMixin):
    context_object_name = 'product'
    model = Product
    template_name = 'products/product.html'
    title = 'geekshop - Каталог'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context
