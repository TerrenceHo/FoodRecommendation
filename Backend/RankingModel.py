import tensorflow as tf
import numpy as np

def genGenericModel(savePath, queries, restDicts, numEpochs, batchSize, learningRate = 0.001):
    numBatches, wideInputFeatures, deepInputFeatures, answers = genInputFeatures(queries, restDicts, batchSize)

    #Define tf model:
    wideFeatures = tf.placeholder(tf.float32, shape=[None, 4])
    deepFeatures = tf.placeholder(tf.float32, shape=[None, 35])
    y = tf.placeholder(tf.float32, shape=[None, 1])


    deepW1 = weight_variable([35, 30], name="deepW1")
    deepB1 = bias_variable([30], name="deepB1")
    deepW2 = weight_variable([30, 20], name="deepW2")
    deepB2 = bias_variable([20], name="deepB2")
    deepW3 = weight_variable([20, 10], name="deepW3")
    deepB3 = bias_variable([10], name="deepB3")
    fc_W = weight_variable([14, 1], name="fc_W")
    fc_B = bias_variable([1], name="fc_B")

    deepLayer1 = tf.nn.relu(tf.matmul(deepFeatures, deepW1) + deepB1)
    deepLayer2 = tf.nn.relu(tf.matmul(deepLayer1, deepW2) + deepB2)
    deepLayer3 = tf.nn.relu(tf.matmul(deepLayer2, deepW3) + deepB3)
    fc_layer = tf.concat([deepLayer3, wideFeatures], 1)
    readout = tf.matmul(fc_layer, fc_W) + fc_B
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=readout))

    trainer = tf.train.AdamOptimizer(learningRate).minimize(loss)
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for e in range(numEpochs):
            lossForEpoch = 0
            for i in range(numBatches):
                _, l = sess.run([trainer, loss], feed_dict={deepFeatures : deepInputFeatures[i], wideFeatures: wideInputFeatures[i], answers[i]})
                lossForEpoch += l
            if e % 10 ==0:
                print("For epoch " + str(e) + ", the cost is " + str(lossForEpoch))

        saver.save(sess, savePath)


def returnTopThree(model, query):
    return None

def retrainOnUpdate():
    return None

def genInputFeatures(queries, restDicts):
    return None

def retreivePossibleRests(query):
    return None

def weight_variable(shape, name=None):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial, name)

def bias_variable(shape, name=None):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial, name)
