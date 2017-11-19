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
global winner
winner = team_data.team_data(0, "", 0, 0, 0)
global loser
loser = team_data.team_data(0, "", 0, 0, 0)
global odds
odds =(0,0)
global t1
t1 = team_data.team_data(0, "", 0, 0, 0)
global t2
t2 = team_data.team_data(0, "", 0, 0, 0)
global t1_pred
t1_pred = team_data.team_data(0, "", 0, 0, 0)
global t2_pred
t2_pred = team_data.team_data(0, "", 0, 0, 0)
def index(request):
    global t1, t2, odds
    bidders = Player.objects.all()
    bidders_by_id = Player.objects.all().order_by('pid')
    teams = Team.objects.all()
    return render(request, 'index.html', {'bidders' : bidders, 'teams' : teams, 'bidders_by_id' : bidders_by_id, 't1' : gm.get_team_name(t1.team_id), 't2' : gm.get_team_name(t2.team_id), 'odds0' : int(odds[0]*100), 'odds1': int(odds[1]*100)})
def start_league(request):
    return render(request, 'start.html')

def confirm_players(request):
    reset_season()
    players = json.loads(request.body.decode('utf-8'))['players']
    pid = 0
    for player in players:
        p = Player(pid = pid, player_name = player, wallet = 500)
        pid +=1
        p.save()
    Team.objects.all().delete()
    all_teams = gm.get_team_dict()
    for team_key, team_name in all_teams.items():
        t = Team(team_name = team_name, team_id=team_key)
        t.save()
    gm.start_new_season(year)
    global t1, t1_pred, t2, t2_pred, odds
    t1, t1_pred, t2, t2_pred, odds = gm.new_match()
    return HttpResponse("Success")

def register_bets(request):
    players = Player.objects.all()
    bets_amount = json.loads(request.body.decode('utf-8'))['bets']
    team_bet = json.loads(request.body.decode('utf-8'))['team_bet']
    global t1, t1_pred, t2, t2_pred, odds, winner, loser
    winner, loser = gm.play_match(t1, t1_pred, t2, t2_pred, odds)
    total_pot = 0
    for bet in bets_amount:
        total_pot += float(bet)

    total_winners=0
    for player in players:
        team = t1.team_id if (float(team_bet[player.pid]) == 0.0) else t2.team_id
        betting.place_bet(player, float(bets_amount[player.pid]), team)
        print ("Current player bets: \n" + player.team_bet +"\n")
        player.save()
        total_winners += 1
    for player in players:
        print ("Resolved player bets: \n" + winner.team_id +"\n")
        betting.resolve_bet(player, winner.team_id, 1+(float(bets_amount[player.pid])/total_pot))
        
        player.save()
    gm.compute_rankings()
    win_team = Team.objects.get(team_id = t1.team_id)
    lose_team = Team.objects.get(team_id = t2.team_id)

    win_team.wins +=1
    lose_team.losses += 1
    win_team.rank = gm.current_season[gm.current_season.index(t1)].rank
    lose_team.rank = gm.current_season[gm.current_season.index(t2)].rank

    win_team.save()
    lose_team.save()
    t1, t1_pred, t2, t2_pred, odds = gm.new_match()
    return HttpResponse("Success")

def reset_season():
    Player.objects.all().delete()