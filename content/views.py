from django.shortcuts import render
from .models import Cinema, News, ShopCategory, ShopProducts


def cinema_list(request):
    cinemas = Cinema.objects.all()

    context = {
        'cinemas': cinemas,
        'page_title': 'Cinemas',
    }
    return render(request, 'content/cinema_list.html', context)

def news_list(request):
    news = News.objects.all()
    context = {
        'news': news,
        'page_title': 'News',
    }

    return render(request, 'content/news.html', context)

def shop_view(request):
    categories = ShopCategory.objects.all().order_by('id')
    products = ShopProducts.objects.all().select_related('category').order_by('id')

    context = {
        'categories': categories,
        'products': products,
        'page_title': 'Shop',
    }
    return render(request, 'content/shop.html', context)