from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

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


def product(request, pk):
    title = 'geekshop - Каталог'
    product_ = get_object_or_404(Product, pk=pk),
    categories = ProductCategory.objects.filter(is_active=True)
    content = {
        'title': title,
        'product': product_[0],
        'categories': categories,
    }

    return render(request, 'products/product.html', content)
