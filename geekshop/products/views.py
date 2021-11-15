from django.shortcuts import render


# Create your views here.
def main(request):
    content = {"title": "geekshop - Главная"}
    return render(request, 'products/index.html', content)


def products(request):
    content = {"title": "geekshop - Каталог",
               "products":
                   [
                       {"img": "Adidas-hoodie.png", "title": "Худи черного цвета с монограммами adidas Originals",
                        "price": "6 090,00", "text": "Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни"},
                       {"img": "Blue-jacket-The-North-Face.png", "title": "Синяя куртка The North Face",
                        "price": "23 725,00", "text": "Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель."},
                       {"img": "Brown-sports-oversized-top-ASOS-DESIGN.png", "title": "Коричневый спортивный oversized-топ ASOS DESIGN",
                        "price": "3 390,00", "text": "Материал с плюшевой текстурой. Удобный и мягкий."},
                       {"img": "Black-Nike-Heritage-backpack.png", "title": "Черный рюкзак Nike Heritage",
                        "price": "2 340,00", "text": "Плотная ткань. Легкий материал."},
                       {"img": "Black-Dr-Martens-shoes.png", "title": "Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex",
                        "price": "13 590,00", "text": "Гладкий кожаный верх. Натуральный материал."},
                       {"img": "Dark-blue-wide-leg-ASOs-DESIGN-trousers.png", "title": "Темно-синие широкие строгие брюки ASOS DESIGN",
                        "price": "2 890,00", "text": "Легкая эластичная ткань сирсакер Фактурная ткань."},
                   ]
               }
    return render(request, 'products/products.html', content)
