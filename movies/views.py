import re

from django.shortcuts import render, get_object_or_404
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


def movie_detail_view(request, movie_id):
    """
    Afiseaza detaliile unui singur film si programul de proiectii asociat,
    inclusiv conversia URL-ului trailerului la formatul embed.
    """
    movie = get_object_or_404(Movie, id=movie_id)

    # --------------------------------------------------------
    # LOGICA NOUA: CONVERSIA URL-ULUI DE YOUTUBE LA EMBED
    # --------------------------------------------------------
    if movie.trailer_url:
        # 1. Cauta ID-ul video in URL-ul standard (watch?v=ID)
        # Folosim re.search pentru a gasi ID-ul video, care este mai robust
        match = re.search(r'(?<=v=)[\w-]+', movie.trailer_url)

        if match:
            video_id = match.group(0)
            # Suprascrie URL-ul cu formatul de embed obligatoriu
            movie.trailer_url = f'https://www.youtube.com/embed/{video_id}'
        # Daca link-ul e deja in format scurt (youtu.be) sau deja embed, nu e nevoie de schimbare.
    # --------------------------------------------------------

    # Preluam toate proiectiile active pentru acest film
    showtimes = ShowTime.objects.filter(
        movie=movie,
        is_active=True,
        start_time__gte=timezone.now()  # Filtreaza doar proiectiile viitoare
    ).order_by('start_time')

    # Structuram proiectiile pe zile (pastram logica ta)
    showtimes_by_day = {}
    for showtime in showtimes:
        # Folosim strftime fara formatare excesiva pentru a simplifica
        day_str = showtime.start_time.strftime("%d %B %Y")
        if day_str not in showtimes_by_day:
            showtimes_by_day[day_str] = []
        showtimes_by_day[day_str].append(showtime)

    context = {
        'movie': movie,
        'showtimes_by_day': showtimes_by_day,
        'page_title': f'{movie.title} | Detalii și Program',
    }

    return render(request, 'movies/movie_detail.html', context)