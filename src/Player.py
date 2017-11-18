class Player:
    def __init__(self, PID=0, wins=0, loses=0, wallet=100, amount_bet=0, team_bet=""):
        self.PID = PID   #The player's ID
        self.wins = wins  #The total number of wins of the player
        self.loses = loses #The total number of losses of the player
        self.wallet = wallet #The player wallet storing how much money they have left to bet
        self.amount_bet = amount_bet #The amount of money the player bet this round
        self.team_bet = team_bet #The team the player is currently betting on
    def __str__(self):
        return "PID: {}\n# Wins: {}\n# Loses: {}\nWallet: {}\nAmount Bet: {}\nTeam Bet: {}\n".format(self.PID, self.wins, self.loses, self.wallet, self.amount_bet, self.team_bet)