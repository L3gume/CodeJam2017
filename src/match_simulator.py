import team_data

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
    def simulate_match(self, cur_team1, pred_team1, cur_team2, pred_team2):
        team_ratings = self.compute_odds(cur_team1, pred_team1, cur_team2, pred_team2)
        cur_team1, cur_team2 = self.determine_winner(team_ratings, cur_team1, cur_team2)
        return cur_team1, cur_team2

    # all args are team_data objects
    # Args:
    # - team 1's current stats
    # - team 1's predicted stats
    # - team 2's current stats
    # - team 2's predicted stats
    # Returns:
    # - A tuple of the two team's ratings
    def compute_odds(self, cur_team1, pred_team1, cur_team2, pred_team2):
        # Get current wins and losses from both teams
        t1_cur_win = cur_team1.wins
        t2_cur_win = cur_team2.wins
        t1_cur_loss = cur_team1.losses
        t2_cur_loss = cur_team2.losses

        # Get predicted wins and losses for teams
        t1_pred_win = pred_team1.wins
        t2_pred_win = pred_team2.wins
        t1_pred_loss = pred_team1.losses
        t2_pred_loss = pred_team2.losses

        # Get the predicted ranks of both teams
        t1_rank = pred_team1.rank
        t2_rank = pred_team2.rank

        # Compute the ratings
        t1_rating = (t2_rank / t1_rank) * ((t1_pred_win / t1_cur_win) * 1.0 - (t1_pred_loss / t1_cur_loss) * 1.0)
        t2_rating = (t1_rank / t2_rank) * ((t2_pred_win / t2_cur_win) * 1.0 - (t2_pred_loss / t2_cur_loss) * 1.0)

        # Do the sigmoid ting
        return (t1_rating, t2_rating)

    # Args:
    # - A tuple with the ratings of the two teams
    # - Team 1's current season stats
    # - Team 2's current season stats
    # Returns:
    # - the two team's current data, updated with win or loss
    #   the first of the two is always the winning team.
    def determine_winner(self, ratings, cur_team1, cur_team2):
        # Get the difference between the two ratings
        # Do a + -b to cover the case where b is negative
        i = 0
        t1_rating = ratings[0]
        t2_rating = ratings[1]

        # if team 2's rating is higher that team 1's, swap them to make everything easier
        if t1_rating < t2_rating:
            t1_rating , t2_rating = t2_rating , t1_rating
            cur_team1 , cur_team2 = cur_team2 , cur_team1

        diff = t1_rating + -1 * t2_rating # Get the difference between the two ratings.

        t1_odds = self.sigmoid(diff)
        t2_odds = 1 - t1_odds

        result = random.randin(1, 101)

        if (result <= t2_odds * 100):
            # team 2 wins
            cur_team2.wins += 1
            cur_team1.losses += 1
            cur_team1 , cur_team2 = cur_team2 , cur_team1 # swap back if t2 won
        else:
            # team 1 wins
            cur_team1.wins += 1
            cur_team2.losses += 1

        return cur_team1, cur_team2 # winning team is always the first one

    # Sigmoid function
    # Returns a value between 0 and 1, representing the odds of a team winning
    # TODO: tune it to better reflect the odds of a team winning the game
    def sigmoid(self, _arg):
        return 0.5 * (1 + _arg / (1 + abs(_arg)))
