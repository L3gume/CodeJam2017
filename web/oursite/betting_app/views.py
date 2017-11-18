from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
def bidding(request):
    return HttpResponse("Bidding")
def start_league(request):
    return render(request, 'start.html')
