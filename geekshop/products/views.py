from django.shortcuts import render
from .models import Product


# Create your views here.
def main(request):
    title = "geekshop - Главная"
    content = {'title': title}

    return render(request, 'products/index.html', content)


def products(request):
    title = 'geekshop - Каталог'
    products = Product.objects.all()
    content = {'title': title, 'products': products}

    return render(request, 'products/products.html', content)
