from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import  login , logout
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)


            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(reverse('home'))
        else:
            form = AuthenticationForm()

        return render(request, "user/login.html", {"form": form})
    return None


def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("home")

    return redirect("home")

def profile_view(request):
    return render(request, "user/profile.html")
