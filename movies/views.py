from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie, ShowTime
from content.models import News

from django.db.models import Exists, OuterRef
def home_page(request):

    now = timezone.now()

    #filmele acuma in  derulare
    now_playing_movies = Movie.objects.filter(
        Exists(
            ShowTime.objects.filter(
                movie = OuterRef('pk'),
                is_active = True,
                start_time__gte = now
            )
        )
    ).distinct()

    #filmele derulate in viitor
    # upcoming_movies = Movie.objects.exclude(
    #     pk__in = OuterRef('pk')
    # ).filter(
    #     release_date__gte = now.date()
    # )
    upcoming_movies = Movie.objects.filter(
        release_date__gt=now.date()
    ).exclude(
        id__in=now_playing_movies.values_list('id', flat=True)
    )

    news = News.objects.all()

    context = {
        'now_playing_movies': now_playing_movies,
        'upcoming_movies': upcoming_movies,
        'banner_image_url': '/static/img/banner.png',
        'news': news,
        'page_title': 'Home',
    }

    return render(request, 'movies/home.html', context)


def movie_list_view(request):
    now = timezone.now()

    # Selectăm doar filmele care au cel puțin un ShowTime activ de acum încolo
    movies_with_program = Movie.objects.filter(
        Exists(
            ShowTime.objects.filter(
                movie=OuterRef('pk'),
                is_active=True,
                start_time__gte=now
            )
        )
    ).order_by('title')

    context = {
        'movies': movies_with_program,
        'page_title': 'Now Playing',
    }
    return render(request, 'movies/movies_showtime_list.html', context)

def all_movies_view(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies,
        'page_title': 'All Movies',
    }

    return render(request, 'movies/movies_list.html', context)

def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    showtimes = ShowTime.objects.filter(
        movie=movie,
        is_active=True,
        start_time__gte=timezone.now()
    ).order_by('start_time')

    # # Structura: { 'Cinema Loteanu': [showtime1, showtime2], 'Cinema Patria': [...] }
    # shows_by_cinema = {}
    # for st in showtimes:
    #     cinema_name = st.hall.cinema.name if st.hall.cinema else "Cinema General"
    #     if cinema_name not in shows_by_cinema:
    #         shows_by_cinema[cinema_name] = []
    #     shows_by_cinema[cinema_name].append(st)
    grouped_data = {}

    for st in showtimes:
        day_label = st.start_time.strftime('%a, %d %b')
        cinema_name = st.hall.cinema.name if st.hall.cinema else "Cinema Patria"

        if day_label not in grouped_data:
            grouped_data[day_label] = {}

        if cinema_name not in grouped_data[day_label]:
            grouped_data[day_label][cinema_name] = []

        grouped_data[day_label][cinema_name].append(st)

    context = {
        'movie': movie,
        # 'shows_by_cinema': shows_by_cinema,
        "grouped_data": grouped_data,
        'page_title': f'{movie.title} | Details and Schedule',
    }

    return render(request, 'movies/movie_detail.html', context)


def booking_view(request, showtime_id):
    return render(request, "movies/booking.html")