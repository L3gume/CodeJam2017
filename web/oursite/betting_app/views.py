from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.core import serializers


def index(request):
    
    return render(request, 'index.html')
def bidding(request):
    return render(request, "index.html")
def start_league(request):
    return render(request, 'start.html')

def confirm_players(request):
    #players = Player.objects.all()
    boii = json.loads(request.body.decode('utf-8'))
    print (boii['players'])
    test= boii['players']

    return HttpResponse(test)
    