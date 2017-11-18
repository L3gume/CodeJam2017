class team_data:
    def __init__(self, _year_id, _team_id, _rank, _wins, _losses):
        self.year_id = _year_id
        self.team_id = _team_id
        self.rank = _rank
        self.wins = _wins
        self.losses = _losses

    def get_total_games(self):
        return self.wins + self.losses
