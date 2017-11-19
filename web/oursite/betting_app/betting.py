from betting_app.models import Player

def place_bet(player, amount, team):
    player.wallet -= amount
    player.amount_bet = amount
    player.team_bet = team

def resolve_bet(player, winning_team, return_factor):
    if(player.team_bet == winning_team):
        player.wallet += player.amount_bet * return_factor
    player.amount_bet = 0
    player.team_bet = ""