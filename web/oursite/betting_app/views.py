from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from betting_app.models import Player
from betting_app.models import Team


def index(request):
    bidders = Player.objects.all()
    teams = Team.objects.all()
    return render(request, 'index.html', {'bidders' : bidders, 'teams' : teams})
def bidding(request):
    return render(request, "index.html")
def start_league(request):
    return render(request, 'start.html')

def confirm_players(request):
    players = json.loads(request.body.decode('utf-8'))['players']
    pid = 0
    for player in players:
        p = Player(pid = pid, player_name = player, wallet = 500)
        pid +=1
        p.save()
    return HttpResponse("Success")
    
