from django.shortcuts import render
from django.utils import timezone
from django.db.models import Min, Count
from .models import Movie, ShowTime

def home_page(request):
    """
    Afișează pagina Home cu o listă a filmelor care au proiecții active,
    corectând numele de relație inversă pentru adnotare.
    """
    now = timezone.now()

    # 1. Filtrează Showtimes: active și viitoare.
    #    (Folosim .select_related('movie') pentru optimizare)
    active_showtimes = ShowTime.objects.filter(
        is_active=True,
    ).select_related('movie')

    # 2. Obține ID-urile unice ale filmelor care au aceste proiecții.
    movie_ids = active_showtimes.values_list('id', flat=True).distinct()

    # 3. Preluăm detaliile filmelor și le adnotăm.
    #    Folosim "showtime_set" ca nume de relație inversă standard
    #    (Dacă "showtime" nu a funcționat)
    movies_with_showtimes = Movie.objects.filter(id__in=movie_ids).annotate(
        min_price=Min('showtime__price'), # <--- Am lăsat "showtime" (numele modelului în lc)
    ).order_by('release_date')

    # NOTĂ IMPORTANTĂ:
    # Dacă *această* versiune (cu 'showtime') nu funcționează,
    # înseamnă că trebuie să folosești numele implicit al relației inverse: 'showtime_set'.
    # În acest caz, liniile 2 și 3 de mai sus ar trebui să fie:
    #
    # min_price=Min('showtime_set__price'),
    # showtime_count=Count('showtime_set')
    #
    # Te rog să încerci ambele variante!

    context = {
        'movies': movies_with_showtimes,
        'page_title': 'Acasă | Filme în Program',
        'mesaj_bun_venit': 'Proiecții disponibile în program:',
    }

    return render(request, 'movies/home.html', context)