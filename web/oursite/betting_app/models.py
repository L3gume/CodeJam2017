from django.db import models

class Player(models.Model):

    pid = models.IntegerField(default = 0)
    player_name = models.CharField(max_length = 32, default = "")
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    wallet = models.IntegerField(default = 0)
    amount_bet = models.IntegerField(default = 0)
    team_bet = models.CharField(max_length = 3, default = "")

    def __str__(self):
        return "PID: {}\nName: {}\n# Wins: {}\n# Loses: {}\nWallet: {}\nAmount Bet: {}\nTeam Bet: {}\n".format(self.pid, self.player_name, self.wins, self.losses, self.wallet, self.amount_bet, self.team_bet)