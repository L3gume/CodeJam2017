import predict_season as sp
import team_data as td
import team_parser as tp
import match_simulator as ms
import game_manager as gm

t = tp.team_parser()
m = ms.match_simulator()
g = gm.game_manager()
np = sp.Season_Predictor()

for i in range(0, 1):
    print(g.team_dict)
    g.start_new_season(2016 + i)

    t1, t2 = g.new_match()
    print(g.get_team_name(t1.team_id))
    print(g.get_team_name(t2.team_id))
    winner, loser = g.play_match(t1, t2)
    print('winner: ' + g.get_team_name(winner.team_id))
    print('loser: ' + g.get_team_name(loser.team_id))
