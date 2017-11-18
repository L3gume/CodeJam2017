class game_simulator:
    # all args are lists of parameters
    def compute_odds(self, cur_team1, pred_team1, cur_team2, pred_team2):
        # Get current wins and losses from both teams
        t1_cur_win = cur_team1[3]
        t2_cur_win = cur_team2[3]
        t1_cur_loss = cur_team1[4]
        t2_cur_loss = cur_team2[4]

        # Get predicted wins and losses for teams
        t1_pred_win = pred_team1[3]
        t2_pred_win = pred_team2[3]
        t1_pred_loss = pred_team1[4]
        t2_pred_loss = pred_team2[4]

        # Get the predicted ranks of both teams
        t1_rank = pred_team1[2]
        t2_rank = pred_team2[2]

        # Compute the ratings
        t1_rating = (t2_rank / t1_rank) * ((t1_pred_win / t1_cur_win) * 1.0 - (t1_pred_loss / t1_cur_loss) * 1.0)
        t2_rating = (t1_rank / t2_rank) * ((t2_pred_win / t2_cur_win) * 1.0 - (t2_pred_loss / t2_cur_loss) * 1.0)

        i = 0
        # Get the difference between the two ratings
        # Do a + -b to cover the case where b is negative
        if t1_rating > t2_rating:
            i = t1_rating + -1 * t2_rating
        else:
            i = t2_rating + -1 * t1_rating

        # Do the sigmoid ting
        return (sigmoid(t1_rating), sigmoid(t2_rating))

    def sigmoid(self, _arg):
        return 0.5 * (1 + _arg / (1 + abs(_arg)))
