import tensorflow as tf
import numpy as np
import team_data as td

class Season_Predictor:
    def __init__(self):
        self.NUM_ITER = 500000
        self.BATCH_SIZE = 50

        self.LEARNING_RATE = 1e-5

        self.NUM_INPUT_NODES = 5
        self.NUM_HIDDEN_NODES = 5
        self.NUM_OUTPUT_NODES = 5

        self.DROPOUT_RATE = 1.0

        self.training_size = 2268
        self.testing_size = 567 #actual value is testing_size - 1 since we are using the "next year" as the label (and no next year for latest data)

        self.model = "Model/season_model"

        self.training_data = []
        self.training_labels = []

        self.testing_data = []
        self.testing_labels = []

        self.generate_training_and_testing_set()

    def next_batch(self, num, data, labels):
        idx = np.arange(0, len(data))
        np.random.shuffle(idx)
        idx = idx[:num]
        data_shuffle = [data[i] for i in idx]
        labels_shuffle = [labels[i] for i in idx]

        return np.asarray(data_shuffle), np.asarray(labels_shuffle)

    def generate_training_and_testing_set(self):
        data_path = "../../data/"

        f = open(data_path + "data.csv", 'r')
        lines = f.readlines() #ignore first line with headers
        last = lines[-1]

        index = 0
        last_line = []
        training = True

        for line in lines:
            #Team, Year, Rank, Win, Loss
            line_data = [int(x) for x in line.rstrip(',\n').split(',')]

            if last_line == []:
                last_line = line_data
                continue
            
            if last_line[0] == line_data[0]: #looking at same team
                if training: #training set
                    if self.training_data == []:
                        self.training_data.append(last_line)

                    self.training_data.append(line_data)

                    if index != 0: #only add label if index is not 0
                        self.training_labels.append(line_data)
                else: #testing set
                    if self.testing_data == []:
                        self.testing_data.append(last_line)

                    if line == last: #if on last line
                        self.testing_labels.append(line_data)
                    else:
                        self.testing_data.append(line_data)

                        if index != 0:
                            self.testing_labels.append(line_data)
            else:
                if (training) & (index > self.training_size): #last training example
                    training = False
                    index = 0

            index += 1
            last_line = line_data
        f.close()

        self.training_data = self.training_data[:-1]
        self.testing_data = self.testing_data[:-1]

        self.training_size = len(self.training_data)
        self.testing_size = len(self.testing_data)

    def train(self):
        x_ = tf.placeholder(tf.float32, shape=[None, self.NUM_INPUT_NODES], name="x_")
        y_ = tf.placeholder(tf.float32, shape=[None, self.NUM_OUTPUT_NODES])

        w_1 = tf.Variable(tf.add(tf.eye(self.NUM_HIDDEN_NODES, dtype=tf.float32), tf.random_uniform([self.NUM_INPUT_NODES, self.NUM_HIDDEN_NODES], -0.1, 0.1)))
        w_2 = tf.Variable(tf.add(tf.eye(self.NUM_OUTPUT_NODES, dtype=tf.float32), tf.random_uniform([self.NUM_HIDDEN_NODES, self.NUM_OUTPUT_NODES], -0.1, 0.1)))
        #w_1 = tf.Variable(tf.eye(self.NUM_HIDDEN_NODES))
        #w_2 = tf.Variable(tf.eye(self.NUM_OUTPUT_NODES))
        #w_1 = tf.Variable(tf.zeros([self.NUM_INPUT_NODES, self.NUM_HIDDEN_NODES]))
        #w_2 = tf.Variable(tf.zeros([self.NUM_HIDDEN_NODES, self.NUM_OUTPUT_NODES]))

        b_1 = tf.Variable(tf.random_uniform([self.NUM_HIDDEN_NODES], 0, 0.1))
        b_2 = tf.Variable(tf.random_uniform([self.NUM_OUTPUT_NODES], 0, 0.1))
        #b_1 = tf.Variable(tf.zeros([self.NUM_HIDDEN_NODES]))
        #b_2 = tf.Variable(tf.zeros([self.NUM_OUTPUT_NODES]))

        h_1 = tf.nn.relu(tf.matmul(x_, w_1) + b_1)

        #Dropout to reduce overfitting
        keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        h_drop = tf.nn.dropout(h_1, keep_prob)

        h_2 = tf.add(tf.matmul(h_drop, w_2), b_2, name="h_2")

        cost = tf.reduce_mean(tf.square(y_ - h_2))

        training_step = tf.train.AdamOptimizer(self.LEARNING_RATE).minimize(cost)

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        cost_summary = tf.summary.scalar('cost', cost)
        summary_op = tf.summary.merge_all()
        test_writer = tf.summary.FileWriter("Graph/Test/", sess.graph)

        for i in range(self.NUM_ITER):
            batch_xs, batch_ys = self.next_batch(self.BATCH_SIZE, self.training_data, self.training_labels)

            if i == 0:
                print('Initial Cost: ', sess.run(cost, feed_dict={x_: self.testing_data, y_: self.testing_labels, keep_prob: 1.0}))

            #training
            sess.run(training_step, feed_dict={x_: batch_xs, y_: batch_ys, keep_prob: self.DROPOUT_RATE})

            #test summary
            summary = sess.run(summary_op, feed_dict={x_: self.testing_data, y_: self.testing_labels, keep_prob: 1.0})
            test_writer.add_summary(summary, i)

        print('Cost: ', sess.run(cost, feed_dict={x_: self.testing_data, y_: self.testing_labels, keep_prob: 1.0}))

        #predictions = sess.run(h_2, feed_dict={x_: self.testing_data, keep_prob: 1.0})
        #print(predictions)

        saver = tf.train.Saver() #create saver that will save all the variables
        saver.save(sess, self.model) #save the model

    def get_data_from_year_and_team(self, year, team):
        for i in range(0, len(self.training_data)):
            if (self.training_data[i][1] == year) & (self.training_data[i][0] == team):
                return self.training_data[i]

        for i in range(0, len(self.testing_data)):
            if (self.testing_data[i][1] == year) & (self.testing_data[i][0] == team):
                return self.testing_data[i]
    
    def get_prediction(self, year, team):
        sess = tf.Session()
        saver = tf.train.import_meta_graph(self.model + ".meta")
        saver.restore(sess, tf.train.latest_checkpoint('./Model/'))

        graph = tf.get_default_graph()

        x_ = graph.get_tensor_by_name("x_:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        h_2 = graph.get_tensor_by_name("h_2:0")

        vals = None
        years_to_predict = 0
        predict_year = year

        while vals == None:
            years_to_predict += 1
            predict_year -= 1
            vals = self.get_data_from_year_and_team(predict_year, team)

        while years_to_predict > 0:
            years_to_predict -= 1
            vals = sess.run(h_2, feed_dict={x_: np.reshape(vals, (1, 5)), keep_prob: 1.0})

        predictions = sess.run(h_2, feed_dict={x_: np.reshape(vals, (1, 5)), keep_prob: 1.0})

        print(predictions)

        pred = td.team_data(year, team, round(predictions[0][2]), round(predictions[0][3]), round(predictions[0][4]))

        return pred