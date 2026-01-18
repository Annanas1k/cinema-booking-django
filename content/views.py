from django.shortcuts import render
from .models import Cinema

def cinema_list(request):
    cinemas = Cinema.objects.all()

    context = {
        'cinemas': cinemas,
        'page_title': 'Cinemas',
    }
    return render(request, 'content/cinema_list.html', context)
