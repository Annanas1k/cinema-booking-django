# from django.shortcuts import render, get_object_or_404
#
# from movies.models import ShowTime
# from .models import Reservation
#
#
# def booking_view(request, hall_id, showtime_id):
#     showtime = get_object_or_404(ShowTime.objects.select_related('movie','hall'),
#                                  id=showtime_id, hall_id=hall_id)
#
#     hall = showtime.hall
#     movie = showtime.movie
#
#     all_seats = showtime.hall.seats.all().order_by('row', 'column')
#
#     occupied_seats_ids = Reservation.objects.filter(
#         showtime = showtime,
#         status__in = ['reserved', 'paid']
#     ).values_list('seat_id', flat=True)
#
#     rows_data = {}
#     for seat in all_seats:
#         if seat.row not in rows_data:
#             rows_data[seat.row] = []
#
#         rows_data[seat.row].append({
#             'id': seat.id,
#             'column': seat.column,
#             'is_occupied': seat.id in occupied_seats_ids,
#             'is_functional': seat.is_functional
#         })
#
#     context = {
#         'showtime': showtime,
#         "rows_data": rows_data,
#         "hall": hall,
#         "movie": movie,
#         "page_title": "Booking",
#     }
#     return render(request, 'reservations/booking_screen.html', context)


import json
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from movies.models import ShowTime
from .models import Reservation
from django.contrib.auth.decorators import login_required

@login_required
def booking_view(request, hall_id, showtime_id):
    showtime = get_object_or_404(ShowTime.objects.select_related('movie','hall'),
                                 id=showtime_id, hall_id=hall_id)

    # --- LOGICA PENTRU SALVARE REZERVARE (POST) ---
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_ids = data.get('seat_ids', [])

            if not seat_ids:
                return JsonResponse({'status': 'error', 'message': 'No seats selected.'}, status=400)

            with transaction.atomic():
                # Verificăm din nou dacă locurile nu s-au ocupat între timp
                already_occupied = Reservation.objects.filter(
                    showtime=showtime,
                    seat_id__in=seat_ids,
                    status__in=['reserved', 'paid']
                ).exists()

                if already_occupied:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'One or more seats have just been taken. Please refresh.'
                    }, status=400)

                # Creăm rezervările
                for s_id in seat_ids:
                    Reservation.objects.create(
                        user=request.user, # Asigură-te că userul e logat
                        showtime=showtime,
                        seat_id=s_id,
                        status='reserved'
                    )

            # URL-ul unde trimiți utilizatorul după succes (ex: pagina de profil sau plată)
            # redirect_url = reverse('reservations:my_reservations')
            return JsonResponse({
                'status': 'success',
                'redirect_url': reverse('booking_success', kwargs={'showtime_id': showtime_id})
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # --- LOGICA PENTRU AFIȘARE PAGINĂ (GET) ---
    all_seats = showtime.hall.seats.all().order_by('row', 'column')
    occupied_seats_ids = Reservation.objects.filter(
        showtime=showtime,
        status__in=['reserved', 'paid']
    ).values_list('seat_id', flat=True)

    rows_data = {}
    for seat in all_seats:
        if seat.row not in rows_data:
            rows_data[seat.row] = []
        rows_data[seat.row].append({
            'id': seat.id,
            'column': seat.column,
            'is_occupied': seat.id in occupied_seats_ids,
            'is_functional': seat.is_functional
        })

    context = {
        'showtime': showtime,
        "rows_data": rows_data,
        "hall": showtime.hall,
        "movie": showtime.movie,
        "page_title": "Booking",
    }
    return render(request, 'reservations/booking_screen.html', context)


def booking_success_view(request, showtime_id):
    showtime = get_object_or_404(ShowTime, id=showtime_id)
    context = {
        "showtime": showtime,
        "page_title": "Success",
    }
    return render(request, 'reservations/booking_success.html', context)