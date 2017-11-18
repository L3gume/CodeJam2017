from Player import Player

player_list = []

def place_bet(player, amount, team):
    player.wallet -= amount
    player.amount_bet = amount
    player.team_bet = team

def resolve_bet(player, winning_team, return_factor):
    if(player.team_bet == winning_team):
        player.wallet += player.amount_bet * return_factor
    player.amount_bet = 0
    player.team_bet = ""

def add_player(player):
    player_list.append(player)

def get_list():
    return player_list

def clear_list():
    player_list.clear()