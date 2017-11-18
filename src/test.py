import predict_season as sp
import team_data as td
import team_parser as tp
import match_simulator as ms
import game_manager as gm

t = tp.team_parser()
m = ms.match_simulator()
g = gm.game_manager()
np = sp.Season_Predictor()

for i in range(0, 5):
    print(g.team_dict)
    np.get_prediction(2016, 'NYY')
    g.start_new_season(2016 + i)

    t1, t2 = g.new_match()
    print(t1)
    print(t2)
    print(play_match(t1, t2))
