from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
def bidding(request):
    boii = request.POST.get('players', None)

    return HttpResponse(boii)
def start_league(request):
    return render(request, 'start.html')
