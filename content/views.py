from django.shortcuts import render
from .models import Cinema, News


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