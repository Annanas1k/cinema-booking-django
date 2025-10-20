from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello, Cinema!</h1><p>Testul funcționează! 🎬</p>")
