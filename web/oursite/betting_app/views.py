from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
from betting_app.models import Player
from betting_app.models import Team
from betting_app import betting
from betting_app import game_manager
from betting_app import team_data

gm = game_manager.game_manager()
year = 2016
winner = ""
loser = ""
global odds
odds =(0,0)
global t1
t1 = team_data.team_data(0, "", 0, 0, 0)
global t2
t2 = team_data.team_data(0, "", 0, 0, 0)
def index(request):
    bidders = Player.objects.all()

    bidders_by_id = Player.objects.all().order_by('pid')
    teams = Team.objects.all()
    return render(request, 'index.html', {'bidders' : bidders, 'teams' : teams, 'bidders_by_id' : bidders_by_id, 't1' : t1.team_id, 't2' : t2.team_id, 'odds0' : odds[0], 'odds1': odds[1]})
def start_league(request):
    return render(request, 'start.html')

def confirm_players(request):
    players = json.loads(request.body.decode('utf-8'))['players']
    pid = 0
    for player in players:
        p = Player(pid = pid, player_name = player, wallet = 500)
        pid +=1
        p.save()
    Team.objects.all().delete()
    gm.start_new_season(year)
    t1, t2, odds = gm.new_match()
    return HttpResponse("Success")

def register_bets(request):
    players = Player.objects.all()
    bets_amount = json.loads(request.body.decode('utf-8'))['bets']
    team_bet = json.loads(request.body.decode('utf-8'))['team_bet']

    gm.play_match(t1, t2, odds)
    total_pot = 0
    for bet in bets_amount:
        total_pot += bet
    
    total_winners=0
    for player in players:
        team = t1 if (team_bet[player.id] == 0) else t2
        betting.place_bet(player, bets_amount[player.pid], team)
        print (player)
        player.save()
        total_winners += 1
    for player in players:
        betting.resolve_bet(player, winner, total_pot/total_winners)
        print (player)
        player.save()
    gm.compute_rankings()
    t1, t2, odds = gm.new_match()
    return HttpResponse("Success")

