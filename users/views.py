from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login , logout
from django.urls import reverse
from users.forms import RegisterForm


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

def profile_view(request):
    return render(request, "users/profile.html")
