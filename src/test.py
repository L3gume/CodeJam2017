import predict_season as sp
import team_data as td
import team_parser as tp

#p = sp.Season_Predictor()
#p.train()

t = tp.team_parser()

np = sp.Season_Predictor()
data = np.get_prediction(1995, t.str_to_nb('WSN'))