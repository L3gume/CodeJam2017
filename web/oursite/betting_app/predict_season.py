import tensorflow as tf
import numpy as np
import team_data as td

class Season_Predictor:
    def __init__(self):
        self.NUM_ITER = 500000  # number of training size
        self.BATCH_SIZE = 50  # number of samples in batch training sets

        self.LEARNING_RATE = 1e-5  # learning rate of the algorithm

        self.NUM_INPUT_NODES = 5  # number of input nodes
        self.NUM_HIDDEN_NODES = 5  # number of hidden nodes
        self.NUM_OUTPUT_NODES = 5  # number of output nodes

        self.training_size = 2268  # number of training examples
        self.testing_size = 567  # number of testing examples
                                 # actual value is testing_size - 1 since we are using the 
                                 # "next year" as the label (and no next year for latest data)

        self.model = "Model/season_model"  # location of the saved trained model

        self.training_data = []  # holds the training data
        self.training_labels = []  # holds the training labels

        self.testing_data = []  # holds the testing data
        self.testing_labels = []  #holds the testing label

        self.generate_training_and_testing_set()  # generates all training and testing sets

    # This method returns a random batch sample of a specified size given
    # the data and labels to randomize into batches
    def next_batch(self, num, data, labels):
        idx = np.arange(0, len(data))
        np.random.shuffle(idx)
        idx = idx[:num]
        data_shuffle = [data[i] for i in idx]
        labels_shuffle = [labels[i] for i in idx]

        return np.asarray(data_shuffle), np.asarray(labels_shuffle)

    # This method generates all the training and testing set data from the dataset
    def generate_training_and_testing_set(self):
        data_path = "../../data/"  # the path to the data csv file

        f = open(data_path + "data.csv", 'r')
        lines = f.readlines()  # ignore first line with headers
        last = lines[-1]  # store last line in order to know when at the end

        index = 0  # holds the current index in either the training or testing set
        prev_line = []
        training = True

        for line in lines:
            #Team, Year, Rank, Win, Loss
            line_data = [int(x) for x in line.rstrip(',\n').split(',')]

            if prev_line == []:
                prev_line = line_data
                continue
            
            if prev_line[0] == line_data[0]:  # looking at same team
                if training:  # training set
                    if self.training_data == []:
                        self.training_data.append(prev_line)

                    self.training_data.append(line_data)

                    if index != 0:  # only add label if index is not 0
                        self.training_labels.append(line_data)
                else:  # testing set
                    if self.testing_data == []:
                        self.testing_data.append(prev_line)

                    if line == last:  # if on last line
                        self.testing_labels.append(line_data)
                    else:
                        self.testing_data.append(line_data)

                        if index != 0:
                            self.testing_labels.append(line_data)
            else:
                if (training) & (index > self.training_size):  # last training example
                    training = False
                    index = 0

            index += 1
            prev_line = line_data
        f.close()

        self.training_data = self.training_data[:-1] # remove the last line since it does not have a corresponding label
        self.testing_data = self.testing_data[:-1]

        self.training_size = len(self.training_data) # reset the size of training and testing sets
        self.testing_size = len(self.testing_data)

    def train(self):
        x_ = tf.placeholder(tf.float32, shape=[None, self.NUM_INPUT_NODES], name="x_")
        y_ = tf.placeholder(tf.float32, shape=[None, self.NUM_OUTPUT_NODES])

        # set weights between input-hidden and hidden-output layers
        w_1 = tf.Variable(tf.add(tf.eye(self.NUM_HIDDEN_NODES, dtype=tf.float32), tf.random_uniform([self.NUM_INPUT_NODES, self.NUM_HIDDEN_NODES], -0.1, 0.1)))
        w_2 = tf.Variable(tf.add(tf.eye(self.NUM_OUTPUT_NODES, dtype=tf.float32), tf.random_uniform([self.NUM_HIDDEN_NODES, self.NUM_OUTPUT_NODES], -0.1, 0.1)))

        # set biases between input-hidden and hidden-output layers
        b_1 = tf.Variable(tf.random_uniform([self.NUM_HIDDEN_NODES], 0, 0.1))
        b_2 = tf.Variable(tf.random_uniform([self.NUM_OUTPUT_NODES], 0, 0.1))

        # first hidden node
        h_1 = tf.nn.relu(tf.matmul(x_, w_1) + b_1)

        # output node
        h_2 = tf.add(tf.matmul(h_1, w_2), b_2, name="h_2")

        # set cost as mean squared error
        cost = tf.reduce_mean(tf.square(y_ - h_2))

        # set the optimizer to Adam Optimizer
        training_step = tf.train.AdamOptimizer(self.LEARNING_RATE).minimize(cost)

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        # setup summary writer in order to follow training
        cost_summary = tf.summary.scalar('cost', cost)
        summary_op = tf.summary.merge_all()
        test_writer = tf.summary.FileWriter("Graph/Test/", sess.graph)

        for i in range(self.NUM_ITER):
            batch_xs, batch_ys = self.next_batch(self.BATCH_SIZE, self.training_data, self.training_labels)

            if i == 0:
                print('Initial Cost: ', sess.run(cost, feed_dict={x_: self.testing_data, y_: self.testing_labels}))

            # training
            sess.run(training_step, feed_dict={x_: batch_xs, y_: batch_ys})

            # test summary
            summary = sess.run(summary_op, feed_dict={x_: self.testing_data, y_: self.testing_labels})
            test_writer.add_summary(summary, i)

        print('Cost: ', sess.run(cost, feed_dict={x_: self.testing_data, y_: self.testing_labels}))

        saver = tf.train.Saver()  # create saver that will save all the variables
        saver.save(sess, self.model)  # save the model

    # Searches the training and testin output for the corresponding team and year data
    def get_data_from_year_and_team(self, year, team):
        for i in range(0, len(self.training_data)):
            if (self.training_data[i][1] == year) & (self.training_data[i][0] == team):
                return self.training_data[i]

        for i in range(0, len(self.testing_data)):
            if (self.testing_data[i][1] == year) & (self.testing_data[i][0] == team):
                return self.testing_data[i]
    
    # Gets predictions based off a given year and team
    def get_prediction(self, year, team):
        sess = tf.Session()  # startup session

        # Load model from model directory
        saver = tf.train.import_meta_graph(self.model + ".meta")
        saver.restore(sess, tf.train.latest_checkpoint('./Model/'))

        # Setup default graph
        graph = tf.get_default_graph()

        # Load x_ for input data
        x_ = graph.get_tensor_by_name("x_:0")

        # Load h_2 for output data
        h_2 = graph.get_tensor_by_name("h_2:0")

        vals = None  # the value to predict
        years_to_predict = 0  # the number of years needed to be obtained from nnet to get specified year
        predict_year = year  # the year to predict

        # Gets the latest data for the team, keeping track of the number of years to predict in order
        # to get the data for the specified year
        while vals == None:
            years_to_predict += 1
            predict_year -= 1
            vals = self.get_data_from_year_and_team(predict_year, team)

        # Predict the data needed to generate final output prediction
        while years_to_predict > 0:
            years_to_predict -= 1
            vals = sess.run(h_2, feed_dict={x_: np.reshape(vals, (1, 5))})

        # Get predictions for specified year
        predictions = sess.run(h_2, feed_dict={x_: np.reshape(vals, (1, 5))})

        # Turn the predictions into the specified team_data object
        pred = td.team_data(year, team, round(predictions[0][2]), round(predictions[0][3]), round(predictions[0][4]))

        return pred