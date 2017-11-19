import csv
from betting_app import team_data as td
from betting_app import match_simulator as ms
from betting_app import predict_season as ps
from betting_app import team_parser as tp

class game_manager:

    def __init__(self):
        self.predictor = ps.Season_Predictor()
        self.t = tp.team_parser()
        self.m = ms.match_simulator()
        self.team_dict = {}
        self.past_seasons = []
        self.current_season = []
        self.current_pred_season = []

        f = open("data/team_names.csv")
        reader = csv.reader(f, delimiter=',')
        self.team_dict = {rows[0]:rows[1] for rows in reader}

    def start_new_season(self, _year):
        self.compute_rankings() # just in case
        self.past_seasons.append(list(self.current_season)) # add the current season to the past seasons list

        new_season = [] # initialize new season list
        new_pred_season = []
        for key in self.team_dict.keys():
            # add new team_data object to current season
            new_season.append(td.team_data(_year, key, 0, 0, 0))
            new_pred_season.append(self.predictor.get_prediction(_year, self.t.str_to_nb(key)))
        self.current_season = new_season # current season becomes new season
        self.current_pred_season = new_pred_season

    # Get team name from the Three letter code
    def get_team_name(self, _arg):
        return self.team_dict[_arg]

    # Compute the rankings by sorting the season list by w/l ratio
    def compute_rankings(self):
        def _key(_arg):
            if _arg.losses == 0:
                _arg.losses = 1 # avoid divide by 0
            return _arg.wins / _arg.losses
        self.current_season.sort(key=_key, reverse=True)
        r = 1
        for t in self.current_season:
            t.rank = r
            r += 1

    # Generate a random match, selecting teams which have the least played matches
    def new_match(self):
        # define the key for sorting
        def _key(_arg):
            return _arg.get_total_matches()
        self.current_season.sort(key=_key)

        # Get the two first teams
        team1 = self.current_season[0]
        team2 = self.current_season[1]

        # Get predicted results for those two teams
        # do the ting
        team1_pred = td.team_data(0, '', 0, 0, 0)
        team2_pred = td.team_data(0, '', 0, 0, 0)

        # find the two teams in the predicted season
        for team in self.current_pred_season:
            if self.t.nb_to_str(team.team_id) == team1.team_id:
                team1_pred = team
            elif self.t.nb_to_str(team.team_id) == team2.team_id:
                team2_pred = team

        odds = self.compute_odds(team1, team1_pred, team2, team2_pred)

        return team1, team2, odds

    # Gets the predicted season results of both teams and simulates the match
    # Return:
    # - winning team
    # - losing team
    def play_match(self, team1, team2, odds):
        winner, loser = self.m.simulate_match(team1, team1_pred, team2, team2_pred, odds)
        return winner, loser


    # all args are team_data objects
    # Args:
    # - team 1's current stats
    # - team 1's predicted stats
    # - team 2's current stats
    # - team 2's predicted stats
    # Returns:
    # - A tuple of the odds of both teams winning
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
        t1_rating = (t2_rank / t1_rank) * ((t1_pred_win / (t1_cur_win + 1)) * 1.0 - (t1_pred_loss / (t1_cur_loss + 1)) * 1.0)
        t2_rating = (t1_rank / t2_rank) * ((t2_pred_win / (t2_cur_win + 1)) * 1.0 - (t2_pred_loss / (t2_cur_loss + 1)) * 1.0)

        # Do a + -b to cover the case where b is negative
        i = 0

        # if team 2's rating is higher that team 1's, swap them to make everything easier
        if t1_rating < t2_rating:
            t1_rating , t2_rating = t2_rating , t1_rating
            cur_team1 , cur_team2 = cur_team2 , cur_team1

        diff = t1_rating + -1 * t2_rating # Get the difference between the two ratings.

        print(diff)
        t1_odds = self.sigmoid(diff)
        t2_odds = 1 - t1_odds
        odds = (t1_odds, t2_odds)
        return odds

    # Sigmoid function
    # Returns a value between 0 and 1, representing the odds of a team winning
    # TODO: tune it to better reflect the odds of a team winning the game
    def sigmoid(self, _arg):
        return 1.00 * (1 / (1 + math.exp(-_arg)))
