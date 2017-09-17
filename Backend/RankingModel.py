import tensorflow as tf
import numpy as np
import geopy.distance
import math
import random
import time
import pythonAPI as pA

#Queries should be a list of dictionaries, with each dictionary containing the parameters of a query
#Form of each individual query: {"lat": LAT, "lon": LON, "cuisine": CUISINETYPE, "price": PRICENUM, "time": DATETIMEOBJECT, "distance", DISTANCE}

#restDicts should be a deep list of dictionaries, with each nested list containing the information of the restaurants retreived for the corresponding queries
#Each restaurant dictionary inside the deep list will be a dictionary containing the info of a particular restaurant (parsed from JSON returned by Zomato)


def trainAndCreateGenericModel(savePath, numEpochs, BatchSize, numSampleQueries=200, learningRate=0.001):
    #Generate Random queries
    queries = None
    #Generate corresponding retreived restaurants
    restDicts = None
    genGenericModel(savePath, queries, restDicts, numEpochs, batchSize, learningRate)
    return None


queryCuisineDict = {"American" : 0, "Italian": 1, "Japanese": 2, "Chinese": 3, "Fast Food": 4, "French": 5, "Mediterranean": 6, "Mexican":7, "Thai":8, "Vietnamese":9, "Indian":10, "Other": 12}
distanceOptions = {"1":0, "5":1, "10":2, "15":3, "20":4, "20+":5}

def genGenericModel(savePath, queries, restDicts, numEpochs, batchSize, learningRate = 0.001):

    #Get input tensors from raw data
    numBatches, wideInputFeatures, deepInputFeatures = genInputFeatures(queries, restDicts, batchSize=batchSize)
    #TODO: Figure out format of answers
    answers = makeAnswers(restDicts, batchSize)

    #Define tf model:
    wideFeatures = tf.placeholder(tf.float32, shape=[None, 3])
    deepFeatures = tf.placeholder(tf.float32, shape=[None, 39])
    y = tf.placeholder(tf.float32, shape=[None, 1])


    deepW1 = weight_variable([39, 30], name="deepW1")
    deepB1 = bias_variable([30], name="deepB1")
    deepW2 = weight_variable([30, 20], name="deepW2")
    deepB2 = bias_variable([20], name="deepB2")
    deepW3 = weight_variable([20, 10], name="deepW3")
    deepB3 = bias_variable([10], name="deepB3")
    fc_W = weight_variable([13, 1], name="fc_W")
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
                _, l = sess.run([trainer, loss], feed_dict={deepFeatures : deepInputFeatures[i], wideFeatures: wideInputFeatures[i], y:answers[i]})
                lossForEpoch += l
            if e % 10 ==0:
                print("For epoch " + str(e) + ", the cost is " + str(lossForEpoch))

        saver.save(sess, savePath)
    print("Completed training generic model")
    print("Model stored at: " + savePath)

def returnTopThree(modelPath, query):
    restDicts = None #REPLACE WITCH RESULT FROM API CALL
    wideInputFeatures, deepInputFeatures = genInputFeatures([query], restDicts)

    #Define tf model:
    wideFeatures = tf.placeholder(tf.float32, shape=[None, 3])
    deepFeatures = tf.placeholder(tf.float32, shape=[None, 39])


    deepW1 = weight_variable([39, 30], name="deepW1")
    deepB1 = bias_variable([30], name="deepB1")
    deepW2 = weight_variable([30, 20], name="deepW2")
    deepB2 = bias_variable([20], name="deepB2")
    deepW3 = weight_variable([20, 10], name="deepW3")
    deepB3 = bias_variable([10], name="deepB3")
    fc_W = weight_variable([13, 1], name="fc_W")
    fc_B = bias_variable([1], name="fc_B")

    deepLayer1 = tf.nn.relu(tf.matmul(deepFeatures, deepW1) + deepB1)
    deepLayer2 = tf.nn.relu(tf.matmul(deepLayer1, deepW2) + deepB2)
    deepLayer3 = tf.nn.relu(tf.matmul(deepLayer2, deepW3) + deepB3)
    fc_layer = tf.concat([deepLayer3, wideFeatures], 1)
    readout = tf.matmul(fc_layer, fc_W) + fc_B
    #loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=readout))

    trainer = tf.train.AdamOptimizer(learningRate).minimize(loss)
    restorer = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        restorer.restore(sess, modelPath)
        readoutLayer= sess.run([readout], feed_dict={deepFeatures : deepInputFeatures, wideFeatures: wideInputFeatures})

    #TODO: After ranking the restaurants, return top 3 (tkae argmax of readout and get coressponding restaurants?)
    return None

def retrainOnUpdate():
    return None

def genInputFeatures(queries, restDicts, batchSize=None):
    deepFeatures = []
    wideFeatures = []
    for i in range(len(queries)):
        query = queries[i]
        retreivedRests = restDicts[i]
        for rest in retreivedRests:
            deepFeatures.append(genDeepFeatures(query, rest))
            wideFeatures.append(genWideFeatures(query, rest))
    #Batchify data
    if (batchSize):
        numBatches, wideFeatures = makeBatch(wideFeatures, batchSize)
        numBatches, deepFeatures = makeBatch(deepFeatures, batchSize)
        return numBatches, wideFeatures, deepFeatures
    return wideFeatures, deepFeatures

def genDeepFeatures(query, rest):
    time = [float ((query["time"].hour * 60 + query["time"].minute * 60) - 720)/ float(720)]
    priceRange = [0,0,0,0]
    assert query["price"] > 0 and query["price"] <= 4
    priceRange[query["price"] - 1] = 1
    queryCuisine = [0,0,0,0,0,0,0,0,0,0,0,0]
    queryCuisine[queryCuisineDict[query["cuisine"]]] = 1
    rating = [(rest["restaurant"]["user_rating"]["aggregate_rating"] -2.5) / 2.5]
    distance = [0,0,0,0,0,0]
    distance[distanceOptions[query["distance"]]] = 1
    distBetween = geopy.distance.vincenty((query["lat"], query["lon"]), (rest["restaurant"]["location"]["latitude"], rest["restaurant"]["location"]["longitude"])).miles
    distBetweenVector = [max(-1, min(1, (distBetween - 15)/14))]
    actualCuisine = [0,0,0,0,0,0,0,0,0,0,0]
    for option in queryCuisineDict.keys():
        if option in rest["restaurant"]["cuisine"]:
            actualCuisine[queryCuisineDict[option]] = 1
    actualPrice = [0,0,0,0]
    actualPrice[rest["restaurant"]["price_range"] - 1] = 1
    return time + priceRange + queryCuisine + rating + distance + distBetweenVector + actualCuisine + actualPrice

def genWideFeatures(query, rest):
    rating = [(rest["restaurant"]["user_rating"]["aggregate_rating"] -2.5) / 2.5]
    distBetween = geopy.distance.vincenty((query["lat"], query["lon"]), (rest["restaurant"]["location"]["latitude"], rest["restaurant"]["location"]["longitude"])).miles
    inRange = [0]
    if (query["distance"] == "1" and distBetween <= 1):
        inRange[0] = 1
    elif (query["distance"] == "5" and distBetween <= 5):
        inRange[0] = 1
    elif (query["distance"] == "10" and distBetween <= 10):
        inRange[0] = 1
    elif (query["distance"] == "15" and distBetween <= 15):
        inRange[0] = 1
    elif (query["distance"] == "20" and distBetween <= 20):
        inRange[0] = 1
    elif (query["distance"] == "20+"):
        inRange[0] = 1
    else:
        raise ValueError
    cuisineMatch = [0]
    if (query["cuisine"] in rest["restaurant"]["cuisine"]):
        cuisineMatch = 1
    return inRange + cuisineMatch + rating

def makeBatch(data, batchSize):
    #TAKE A 2-D List shape = (numData, x) and reshape to (numBatches, batchSize, x)
    batches = []
    for batchNum in range(float(np.ceil(len(data))/batchSize)):
        batch = []
        for i in range(batchNum*batchSize, min(len(data), (batchNum+1))*batchSize)
            batch.append(data[i])
        batches.append(batch)
    return batches

def makeAnswers(restDicts, batchSize):
    answers = []
    for retreivedRests in restDicts:
        popularityRatings = []
        for i, rest in enumerate(retreivedRests):
            rating = [(rest["restaurant"]["user_rating"]["aggregate_rating"] -2.5) / 2.5]
            popularityRatings[i] = rating * int(rest["restaurant"]["user_rating"]["votes"])
        popularityRatings = np.array(popularityRatings)
        bestIndices = popularityRatings.argsort()[-3:][::-1]
        answer = [[0] for i in range(len(retreivedRests))]
        for index in bestIndices:
            anwer[index][0] = 1
        answers.extend(answer)
    return answers
    if (batchSize):
        numBatches, anwers = makeBatch(answers, batchSize)
    return answers

def retreivePossibleRests(query):
    #CALL ALEXS SHIT HERE
    return None

def weight_variable(shape, name=None):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial, name)

def bias_variable(shape, name=None):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial, name)

 def genRandomQueries(amount):
    def strTimeProp(start, end, format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))


    def randomDate(start, end, prop):
        return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)

    #lat
    #lon
    #Cuisine
    #price
    #time
    #distance

    for x in range(amount):
      testDict = {}
      cuisineTable = ['American','Chinese','Fast Food','French','Italian','Japanese','Mediterranean','Mexican','Thai','Vietnamese','Indian']
      distanceTable  = ['1','5','10','15','20','20+']
      testDict["lat"] = str(random.uniform(-80.517495,-80.49351))
      testDict["lon"] = str(random.uniform(43.457147,43.50356))
      testDict["cuisine"] = cuisineTable[random.randint(0,10)]
      testDict["price"] = random.randint(1,4)
      testDict["time"] = randomDate("1/1/2008 12:00 AM", "1/1/2008 11:59 PM", random.random())
      testDict["distance"] = distanceTable[random.randint(0,5)]
      return testDict
