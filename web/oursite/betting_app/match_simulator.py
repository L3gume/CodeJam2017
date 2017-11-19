import random
from betting_app import team_data
import math

# Handles simulating games using stats given by the predictive AI
# ONLY USE THE simulate_game FUNCTION
class match_simulator:

    # Simulates a game
    # all args are team_data objects
    # Args:
    # - team 1's current stats
    # - team 1's predicted stats
    # - team 2's current stats
    # - team 2's predicted stats
    # Returns:
    # - winning team
    # - losing team
    def simulate_match(self, cur_team1, pred_team1, cur_team2, pred_team2, odds):
        winner, loser = self.determine_winner(odds, cur_team1, cur_team2)
        return winner, loser

    # Args:
    # - A tuple with the odds of each team winning
    # - Team 1's current season stats
    # - Team 2's current season stats
    # Returns:
    # - the two team's current data, updated with win or loss
    #   the first of the two is always the winning team.
    def determine_winner(self, odds, cur_team1, cur_team2):

        result = random.randrange(1, 101)

        if (result <= odds[1] * 100):
            # team 2 wins
            cur_team2.wins += 1
            cur_team1.losses += 1
            cur_team1 , cur_team2 = cur_team2 , cur_team1 # swap back if t2 won
        else:
            # team 1 wins
            cur_team1.wins += 1
            cur_team2.losses += 1

        return cur_team1, cur_team2 # winning team is always the first one

