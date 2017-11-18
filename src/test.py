import predict_season as sp
import team_data as td
import team_parser as tp

t = tp.team_parser()

np = sp.Season_Predictor()
data = np.get_prediction(2016, t.str_to_nb('WSN'))
data = np.get_prediction(2016, t.str_to_nb('ARI'))
data = np.get_prediction(2016, t.str_to_nb('NYY'))
data = np.get_prediction(2016, t.str_to_nb('NYM'))
data = np.get_prediction(2016, t.str_to_nb('ANA'))
data = np.get_prediction(2016, t.str_to_nb('STL'))
