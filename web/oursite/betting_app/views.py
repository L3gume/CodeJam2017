from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    boii = "hello"
    return render(request, 'index.html', {"myVar": boii})
def betting(request):
    return HttpResponse("Betting")
def start_league(request):
    return render(request, 'start.html')
