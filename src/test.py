import predict_season as sp

tf = sp.Season_Predictor()
tf.generate_training_and_testing_set()
tf.train()
#print(tf.get_prediction(2018, 837678))
