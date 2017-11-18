import csv
import team_data as td
import match_simulator as ms
import predict_season as ps

class game_manager:

    def __init__(self):
        self.predictor = ps.predict_season()
        self.team_dict = {}
        self.past_seasons = []
        self.current_season = []
        self.current_pred_season = []

        f = open("../data/team_names.csv")
        reader = csv.reader(f, delimiter=',')
        self.team_dict = {rows[0]:rows[1] for rows in reader}

    def start_new_season(self, _year):
        self.compute_rankings() # just in case
        past_seasons.append(current_season) # add the current season to the past seasons list

        new_season = [] # initialize new season list
        new_pred_season = []
        for team in team_dict:
            # add new team_data object to current season
            new_season.append(td.team_data(_year, team, 0, 0, 0))
            new_pred_season.append(predictor.get_prediction(_year, team))
        self.current_season = new_season # current season becomes new season
        self.current_pred_season = new_pred_season

    # Get team name from the Three letter code
    def get_team_name(self, _arg):
        return self.team_dict[_arg]

    # Compute the rankings by sorting the season list by w/l ratio
    def compute_rankings(self):
        def _key(_arg):
            return _arg.wins / _arg.losses
        self.current_season.sort(key=_key, reverse=true)
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

        return team1, team2

    # Gets the predicted season results of both teams and simulates the match
    # Return:
    # - winning team
    # - losing team
    def play_match(self, team1, team2):
        # Get predicted results for those two teams
        # do the ting
        team1_pred = none
        team2_pred = none

        # find the two teams in the predicted season
        for team in current_pred_season:
            if team.team_id == team1.team_id:
                team1_pred = team
            elif team.team_id == team2.team_id:
                team2_pred = team

        return ms.simulate_match(team1, team1_pred, team2, team2_pred)
