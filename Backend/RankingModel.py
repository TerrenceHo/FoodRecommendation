import tensorflow as tf
import numpy as np
import geopy.distance
import math
import random
import time
import datetime
import pythonAPI as pA
from zomato import Zomato
import urllib2
import json
from pprint import pprint

#Queries should be a list of dictionaries, with each dictionary containing the parameters of a query
#Form of each individual query: {"lat": LAT, "lon": LON, "cuisine": CUISINETYPE, "price": PRICENUM, "time": DATETIMEOBJECT, "distance", DISTANCE}

#restDicts should be a deep list of dictionaries, with each nested list containing the information of the restaurants retreived for the corresponding queries
#Each restaurant dictionary inside the deep list will be a dictionary containing the info of a particular restaurant (parsed from JSON returned by Zomato)

APIKEY = ["eb3ef3ed91484343e952b92c1a9a626f"]
validKeys = ["021f7c05ee9f665a3661b8e8b5ade5b4", "66b9ba98643878c90ceca5562236fb86", "1577d3dd8d8b5c7d0b1e5bc5892696c2", "4197a02f11307b726dc4b808a66f316f", "6962b9046e25b8ec8df6c4eaa217b1a6", "4ab5541298fc6740c430e7759bd15d99", "c1d1bc9d4fea4ce5c41482488c0bdc83", "6dbd256a23390a7df501c15bf2a082ad", "aaabf864d2828df6c03f4778ece6a180", "99edda14ed75fda14b5fd5896531fb50", "054510a8e612e6dbcae38272e1d30585", "b2fe2d9f8f52ebe38264dcc56ff8716d", "7d275af62ba3f3ba4b7db34e04cc242d", "a24116cbc0a89daefeb0ba45f7d57249", "8389f312b8c53950fa647c26f3b85bba", "c2110c5b434d840a6481f09a7fab2900", "58174b108c884e285f82ad10c3d876ad", "549d5e031d67e3cc9c635548a9aff9c5", "139eb3f37902443ebf59841aa70caa0d", "57bf0edc2491633a3de14d07d9b75148"]
def trainAndCreateGenericModel(savePath, numEpochs=100, batchSize=400, numSampleQueries=150, learningRate=0.001, restoreVars=False, restorePath=None):
    #Generate Random queries
    queries = genRandomQueries(numSampleQueries)
    #Generate corresponding retreived restaurants
    restDicts = []
    for query in queries:
        restDicts.append(queryAccept(query))
    print(restDicts)
    genGenericModel(savePath, queries, restDicts, numEpochs, batchSize, learningRate, restoreVars, restorePath)
    print("Finsihed Training")
    return None

queryCuisineDict = {"American" : 0, "Italian": 1, "Japanese": 2, "Chinese": 3, "Fast Food": 4, "French": 5, "Mediterranean": 6, "Mexican":7, "Thai":8, "Vietnamese":9, "Indian":10, "Other": 12}
distanceOptions = {"1":0, "5":1, "10":2, "15":3, "20":4, "20+":5}

def genGenericModel(savePath, queries, restDicts, numEpochs, batchSize, learningRate = 0.001, restoreVars=False, restorePath=None):

    #Get input tensors from raw data
    numBatches, wideInputFeatures, deepInputFeatures = genInputFeatures(queries, restDicts, batchSize=batchSize)
    #TODO: Figure out format of answers
    answers = makeAnswers(restDicts, batchSize)
    answers = np.array(answers)
    print(answers.shape)

    #Define tf model:
    wideFeatures = tf.placeholder(tf.float32, shape=[None, 3])
    deepFeatures = tf.placeholder(tf.float32, shape=[None, 40])
    y = tf.placeholder(tf.float32, shape=[None, 1])


    deepW1 = weight_variable([40, 30], name="deepW1")
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
    restorer = tf.train.Saver()

    print("Started Training")
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        if (restoreVars):
            restorer.restore(sess, restorePath)
        for e in range(numEpochs):
            lossForEpoch = 0
            for i in range(numBatches):
                _, l = sess.run([trainer, loss], feed_dict={deepFeatures : deepInputFeatures[i], wideFeatures: wideInputFeatures[i], y:answers[i]})
                lossForEpoch += l
            if e % 5 ==0 and e > 0:
                APIKEY.append(validKeys[e/5])
            if e % 10 ==0:
                print("For epoch " + str(e) + ", the cost is " + str(lossForEpoch))
                saver.save(sess, savePath)
                print("Saved model at " + savePath)
        saver.save(sess, savePath)
    print("Completed training generic model")
    print("Model stored at: " + savePath)

def returnTopThree(modelPath, query):
    restDicts = queryAccept(query) #REPLACE WITH RESULT FROM API CALL
    wideInputFeatures, deepInputFeatures = genInputFeatures([query], restDicts)

    #Define tf model:
    wideFeatures = tf.placeholder(tf.float32, shape=[None, 3])
    deepFeatures = tf.placeholder(tf.float32, shape=[None, 40])


    deepW1 = weight_variable([40, 30], name="deepW1")
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
    restorer = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        restorer.restore(sess, modelPath)
        readoutLayer= sess.run([readout], feed_dict={deepFeatures : deepInputFeatures, wideFeatures: wideInputFeatures})

    bestIndices = readoutLayer.argsort()[-3:][::-1]
    recommendations = []
    for index in bestIndices:
        recommendations.append({"name" :restDicts[i]["restaurant"]["name"], "address" : restDicts[i]["restaurant"]["location"]["address"]})
    return recommendations

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
    print((rest))
    rating = [(float(rest["restaurant"]["user_rating"]["aggregate_rating"]) -2.5) / 2.5]
    distance = [0,0,0,0,0,0]
    distance[distanceOptions[query["distance"]]] = 1
    distBetween = geopy.distance.vincenty((query["lat"], query["lon"]), (rest["restaurant"]["location"]["latitude"], rest["restaurant"]["location"]["longitude"])).miles
    distBetweenVector = [max(-1, min(1, (distBetween - 15)/14))]
    actualCuisine = [0,0,0,0,0,0,0,0,0,0,0]
    for option in queryCuisineDict.keys():
        if option in rest["restaurant"]["cuisines"]:
            actualCuisine[queryCuisineDict[option]] = 1
    actualPrice = [0,0,0,0]
    actualPrice[rest["restaurant"]["price_range"] - 1] = 1
    return time + priceRange + queryCuisine + rating + distance + distBetweenVector + actualCuisine + actualPrice

def genWideFeatures(query, rest):
    rating = [(float(rest["restaurant"]["user_rating"]["aggregate_rating"]) -2.5) / 2.5]
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
    cuisineMatch = [0]
    if (query["cuisine"] in rest["restaurant"]["cuisines"]):
        cuisineMatch[0] = 1
    return inRange + cuisineMatch + rating

def makeBatch(data, batchSize):
    #TAKE A 2-D List shape = (numData, x) and reshape to (numBatches, batchSize, x)
    batches = []
    for batchNum in range(int(float(np.ceil(len(data))/batchSize))):
        batch = []
        for i in range(batchNum*batchSize, min(len(data), (batchNum+1)*batchSize)):
            batch.append(data[i])
        batches.append(batch)
    return len(batches), batches

def makeAnswers(restDicts, batchSize):
    answers = []
    for retreivedRests in restDicts:
        popularityRatings = []
        for rest in retreivedRests:
            rating = [(float(rest["restaurant"]["user_rating"]["aggregate_rating"]) -2.5) / 2.5]
            popularityRatings.append(rating * int(rest["restaurant"]["user_rating"]["votes"]))
        popularityRatings = np.array(popularityRatings)
        bestIndices = popularityRatings.argsort()[-3:][::-1]
        answer = [[0] for i in range(len(retreivedRests))]
        for index in bestIndices:
            answer[index][0] = 1
        answers.extend(answer)
    if (batchSize):
        numBatches, answers = makeBatch(answers, batchSize)
    return answers

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
    queries = []
    for x in range(amount):
        testDict = {}
        cuisineTable = ['American','Chinese','Fast Food','French','Italian','Japanese','Mediterranean','Mexican','Thai','Vietnamese','Indian']
        distanceTable  = ["1","5","10","15","20","20+"]
        testDict["lat"] = str(random.uniform(43.457147,43.50356))
        testDict["lon"] = str(random.uniform(-80.517495,-80.49351))
        testDict["cuisine"] = cuisineTable[random.randint(0,10)]
        testDict["price"] = random.randint(1,4)
        testDict["time"] = datetime.time(random.randint(0,23), random.randint(0,59), random.randint(0,59))
        testDict["distance"] = distanceTable[random.randint(0,5)]
        queries.append(testDict)
    return queries

from zomato import Zomato
import urllib2
import json
from pprint import pprint

def cuisineTranslate(cuisine):
    return {
            'American': '1',
            'Chinese': '25',
            'Fast Food': '40',
            'French': '45',
            'Italian': '55',
            'Japanese': '60',
            'Mediterranean': '70',
            'Mexican': '73',
            'Thai': '95',
            'Vietnamese': '99',
            'Indian': '148',
            }.get(cuisine, '')

#Within ~100ft or .004 of a degree
#Pass lat long every 30 seconds to array, remove oldest if does average not fufill deviation of .004 degree
#pastLocations


def queryAccept(query):

    #Variable Declaration
    searchLat = ""
    searchLon = ""
    cuisineType = ""
    priceLevel = ""
    searchDistance = "1"

    for key in query:
        if key == "lat":
            searchLat = str(query["lat"])
        elif key == "lon":
            searchLon = str(query["lon"])
        elif key == "cuisine":
            cuisineType = cuisineTranslate(query["cuisine"])
        elif key == "price":
            priceLevel = str(query["price"])
        elif key == "distance":
            if query["distance"] == "20+":
                searchDistance = str(24 * 1609)
            else:
                searchDistance = str(int(query["distance"]) * 1609)
        elif key == "time":
            '''
                  distanceRef = {"1":1, "5":5, "10":10, "15":15, "20":20, "20+":24}
                  searchLat = str(lat)
                  searchLon = str(lon)
                  cuisineType = cuisineTranslate(cuisine) #check against array and convert to numerical value
                  searchdistance = str(distance * 1609) #distance will be in km, Zomato api needs in meters
                  #creates query needed for Zomato
            '''
    restQuery = "lat=" + searchLat + ", lon=" + searchLon + ", radius =" + searchDistance + ", cuisines=" + cuisineType
    restKey = Zomato(APIKEY[-1])
    restJSON = restKey.parse("search", restQuery)
    if not restJSON:
        return None
    return restJSON["restaurants"]
"""
def querySave(query):
    #Variable Declaration
	currLat = ""
	currLon = ""
	searchLon = ""
	cuisineType = ""
	priceLevel = ""
	searchDistance = "24"
	restaurantName = ""

	for key in query:
        if key == "lat":
            currLat = str(query["lat"]) + ""
        elif key == "lon":
            currLon = str(query["lon"])
        elif key == "cuisine":
            cuisineType = cuisineTranslate(query["cuisine"])
        elif key == "q":
            restaurantName = query["q"]
        elif key == "distance":
            searchDistance = str(24*1609)
    restQuery = "lat=" + searchLat + ", lon=" + searchLon + ", q=" + restaurantName + ", radius=" + searchDistance + ", cuisines=" + cuisineType
    restKey = Zomato("309bf0bce94239a8585b1b209da93a3d")
    restJSON = restKey.parse("search", restQuery)
    return restJSON[0]

def queryRandom(query):
    currLat = ""
 	currLon = ""

 	for key in query:
 		if key == "lat":
 			currLat = str(query["lat"])
 		elif key == "lon":
 			currLon = str(query["lon"])
 	restQuery = "lat=" + searchLat + ", lon=" + searchLon + ", radius=38616, order=asc, sort=real_distance"
 	restKey = Zomato("309bf0bce94239a8585b1b209da93a3d")
 	restJSON = restKey.parse("search", restQuery)
 	randRest = restJSON[random.randint(0, len(restJSON) - 1)]
 	return randRest


#distance = {"1":1, "5":5, "10":10, "15":15, "20":20, "20+":24}
"""
