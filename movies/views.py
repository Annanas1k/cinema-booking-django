from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min, Count
from .models import Movie, ShowTime

def home_page(request):

    now = timezone.now()

    active_showtimes = ShowTime.objects.filter(
        is_active=True,
    ).select_related('movie')

    movie_ids = active_showtimes.values_list('id', flat=True).distinct()

    movies_with_showtimes = Movie.objects.filter(id__in=movie_ids).annotate(
        min_price=Min('showtime__price'),
    ).order_by('release_date')


    # min_price=Min('showtime_set__price'),
    # showtime_count=Count('showtime_set')


    context = {
        'movies': movies_with_showtimes,
        'page_title': 'Acasă | Filme în Program',
        'mesaj_bun_venit': 'Proiecții disponibile în program:',
    }

    return render(request, 'movies/home.html', context)


def movie_list_view(request):
    all_movies = Movie.objects.all().order_by('title')

    context = {
        'movies': all_movies,
        'page_title': 'Toate Filmele',
    }
    return render(request, 'movies/movies_list.html', context)