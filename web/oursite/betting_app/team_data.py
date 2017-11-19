class team_data:
    def __init__(self):
        self.year_id = 0
        self.team_id = ''
        self.rank = 0
        self.wins = 0
        self.losses = 0

    def __init__(self, _year_id, _team_id, _rank, _wins, _losses):
        self.year_id = _year_id
        self.team_id = _team_id
        self.rank = _rank
        self.wins = _wins
        self.losses = _losses

    def get_total_matches(self):
        return self.wins + self.losses
