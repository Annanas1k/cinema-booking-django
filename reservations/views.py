from django.shortcuts import render, get_object_or_404

from movies.models import ShowTime
from .models import Reservation


def booking_view(request, hall_id, showtime_id):
    showtime = get_object_or_404(ShowTime, id=showtime_id, hall_id=hall_id)

    all_seats = showtime.hall.seats.all().order_by('row', 'column')

    occupied_seats_ids = Reservation.objects.filter(
        showtime = showtime,
        status__in = ['reserved', 'paid']
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
    }
    return render(request, 'reservations/booking_screen.html', context)