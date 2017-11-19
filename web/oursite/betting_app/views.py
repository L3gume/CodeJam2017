from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from betting_app.models import Player

def index(request):
    return render(request, 'index.html')
def bidding(request):
    return render(request, "index.html")
def start_league(request):
    return render(request, 'start.html')

def confirm_players(request):
    players = json.loads(request.body.decode('utf-8'))['players']
    for player in players:
        pid = 0
        p = Player(pid = pid, player_name = player, wallet = 500)
        pid +=1
        p.save()
    
