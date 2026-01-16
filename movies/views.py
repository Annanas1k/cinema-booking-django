from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Movie, ShowTime

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
    uncoming_movies = Movie.objects.exclude(
        pk__in = OuterRef('pk')
    ).filter(
        release_date__gte = now.date()
    )

    context = {
        'now_playing_movies': now_playing_movies,
        'uncoming_movies': uncoming_movies,
        'banner_image_url': '/static/img/banner.png',
        'page_title': 'Home'
    }

    return render(request, 'movies/home.html', context)


def movie_list_view(request):
    all_movies = Movie.objects.all().order_by('title')

    context = {
        'movies': all_movies,
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

    showtimes_by_day = defaultdict(list)

    for showtime in showtimes:
        show_date = showtime.start_time.date()

        day_name = show_date.strftime("%A, %d %B %Y").upper()

        showtimes_by_day[day_name].append(showtime)

    context = {
        'movie': movie,
        'showtimes_by_day': dict(showtimes_by_day),
        'page_title': f'{movie.title} | Details and Schedule',
    }

    return render(request, 'movies/movie_detail.html', context)


def booking_view(request, showtime_id):
    return render(request, "movies/booking.html")