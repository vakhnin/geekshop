import json
import os

from django.shortcuts import render


# Create your views here.
def main(request):
    content = {"title": "geekshop - Главная"}
    return render(request, 'products/index.html', content)


def products(request):
    with open('products' + os.sep + 'fixtures' + os.sep + 'products-data.json', 'r',
              encoding="utf-8") as json_file:
        content = json.load(json_file)
        content['title'] = 'geekshop - Каталог'
    return render(request, 'products/products.html', content)
