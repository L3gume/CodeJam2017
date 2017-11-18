from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
def betting(request):
    return HttpResponse("Betting")
def start_league(request):
    return render(request, 'start.html')