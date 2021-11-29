from django.shortcuts import render, get_object_or_404

from .models import Product, ProductCategory


# Create your views here.
def main(request):
    title = "geekshop - Главная"
    content = {'title': title}

    return render(request, 'products/index.html', content)


def products(request):
    title = 'geekshop - Каталог'
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    content = {
        'title': title,
        'products': products,
        'categories': categories,
    }

    return render(request, 'products/products.html', content)


def product(request, id):
    title = 'geekshop - Каталог'
    product_ = get_object_or_404(Product, id=id),
    categories = ProductCategory.objects.all()
    content = {
        'title': title,
        'product': product_[0],
        'categories': categories,
    }

    return render(request, 'products/product.html', content)
