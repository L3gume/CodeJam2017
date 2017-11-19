from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from betting_app.models import Player
from betting_app.models import Team
from betting_app.models import Game_Stats
import betting
import game_manager

gm = game_manager.game_manager()
year = 2016

def index(request):
    bidders = Player.objects.all()
    #bidders_by_id = sorted(bidders, key=sort_player)
    bidders_by_id = Player.objects.all().order_by('-pid')
    teams = Team.objects.all()
    return render(request, 'index.html', {'bidders' : bidders, 'teams' : teams, 'bidders_by_id' : bidders_by_id})
def bidding(request):
    t1, t2 = gm.new_match()
    winner, loser, odds()
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
    gm.start_new_season(year)

    return HttpResponse("Success")

def register_bets(request):
    players = Player.objects.all()
    bets_amount = json.loads(request.body.decode('utf-8'))['bets']
    team_bet = json.loads(request.body.decode('utf-8'))['team_bet']
    
    for player in players:
        betting.place_bet(player, bets_amount[player.pid], team_bet[player.pid])
        betting.resolve_bet(player, winning_team, return_factor)
