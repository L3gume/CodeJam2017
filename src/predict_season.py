import tensorflow as tf
import numpy as np

class Season_Predictor:
    def __init__(self):
        self.NUM_ITER = 50000
        self.BATCH_SIZE = 50

        self.LEARNING_RATE = 1e-3

        self.NUM_INPUT_NODES = 5
        self.NUM_HIDDEN_NODES = 5
        self.NUM_OUTPUT_NODES = 5

        self.DROPOUT_RATE = 0.5

        self.model = "Model/season_model"

    def next_batch(self, num, data, labels):
        idx = np.arange(0, len(data))
        np.random.shuffle(idx)
        idx = idx[:num]
        data_shuffle = [data[i] for i in idx]
        labels_shuffle = [labels[i] for i in idx]

        return np.asarray(data_shuffle), np.asarray(labels_shuffle)

    def generate_training_and_testing_set(self):
        data_path = "../data/"
        self.training_size = 3
        self.testing_size = 2 #actual value is testing_size - 1 since we are using the "next year" as the label (and no next year for latest data)

        self.training_data = [None] * self.training_size
        self.training_labels = [None] * self.training_size

        self.testing_data = [None] * (self.testing_size - 1)
        self.testing_labels = [None] * (self.testing_size - 1)

        f = open(data_path + "data.csv", 'r')
        lines = f.readlines()

        index = 0
        for line in lines:
            if index < self.training_size:
                line_data = [int(x) for x in line.rstrip(',\n').split(',')]

                self.training_data[index] = line_data

                if index != 0:
                    self.training_labels[index - 1] = line_data
            else:
                line_data = [int(x) for x in line.rstrip(',\n').split(',')]

                if index == self.training_size:
                    self.training_labels[index - 1] = line_data

                if index == self.training_size + self.testing_size - 1:
                    self.testing_labels[index - self.training_size - 1] = line_data
                else:
                    self.testing_data[index - self.training_size] = line_data
                    self.testing_labels[index - self.training_size - 1] = line_data
            index += 1
        f.close()

    def train(self):
        self.generate_training_and_testing_set()

        x_ = tf.placeholder(tf.float32, shape=[None, self.NUM_INPUT_NODES], name="x_")
        y_ = tf.placeholder(tf.float32, shape=[None, self.NUM_OUTPUT_NODES])

        w_1 = tf.Variable(tf.zeros([self.NUM_INPUT_NODES, self.NUM_HIDDEN_NODES]))
        w_2 = tf.Variable(tf.zeros([self.NUM_HIDDEN_NODES, self.NUM_OUTPUT_NODES]))

        b_1 = tf.Variable(tf.zeros([self.NUM_HIDDEN_NODES]))
        b_2 = tf.Variable(tf.zeros([self.NUM_OUTPUT_NODES]))

        h_1 = tf.nn.relu(tf.matmul(x_, w_1) + b_1)

        #Dropout to reduce overfitting
        keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        h_drop = tf.nn.dropout(h_1, keep_prob)

        h_2 = tf.add(tf.matmul(h_drop, w_2), b_2, name="h_2")

        cost = tf.reduce_mean(tf.square(y_ - h_2))

        training_step = tf.train.AdamOptimizer(self.LEARNING_RATE).minimize(cost)

        correct_prediction = tf.equal(tf.argmax(h_2, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        cost_summary = tf.summary.scalar('cost', cost)
        accuracy_summary = tf.summary.scalar('accuracy', accuracy)
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

        saver = tf.train.Saver() #create saver that will save all the variables
        saver.save(sess, self.model) #save the model

    def get_data_from_year_and_team(self, year, team):
        for i in range(0, len(self.training_data)):
            if i[0] == year & i[1] == team:
                return i

        for i in range(0, len(self.testing_data)):
            if i[0] == year & i[1] == team:
                return i
    
    def get_prediction(self, year, team):
        sess = tf.Session()
        saver = tf.train.import_meta_graph(self.model + ".meta")
        saver.restore(sess, tf.train.latest_checkpoint('./'))

        graph = tf.get_default_graph()

        x_ = graph.get_tensor_by_name("x_:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        h_2 = graph.get_tensor_by_name("h_2:0")

        vals = [year, team]

        predictions = sess.run(h_2, feed_dict={x_: vals, keep_prob: 1.0})

        print(predictions)

        return predictions