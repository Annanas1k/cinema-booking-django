from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login , logout
from django.urls import reverse
from django.utils import timezone

from users.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(reverse('home'))
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'page_title': 'Login',
    }
    return render(request, "user/login.html", context)


def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("home")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        "form": form,
        'page_title': 'Registration',
    }
    return render(request, "users/register.html", context)

@login_required(login_url='users/login/')
def profile_view(request):
    if request.method == "POST" and 'cancel_reservation_id' in request.POST:
        res_id = request.POST.get('cancel_reservation_id')
        reservation = get_object_or_404(Reservation, id=res_id, user=request.user)
        reservation.delete()
        return redirect('profile')

    user_reservations = Reservation.objects.filter(user=request.user).select_related(
        'showtime__movie',
        'showtime__hall',
        'seat'
    ).order_by('-showtime__start_time')

    context = {
        "reservations": user_reservations,
        "now": timezone.now(),
        'active_tickets_count': user_reservations.filter(showtime__start_time__gte=timezone.now()).count(),
        "page_title": "My Profile",
    }


    return render(request, "users/profile.html", context)
