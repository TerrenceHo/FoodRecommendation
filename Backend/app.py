import os
import json
import datetime

import boto3
from shutil import copyfile

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from RankingModel import *


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.environ.get("DATABASE_URL") is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/food_recommendation'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    tf_path = db.Column(db.String(500))
    num_dollars = db.Column(db.Integer)
    max_distance = db.Column(db.Integer)
    fav_cuisine = db.Column(db.String(200))

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.tf_path = ''

    def create_path(self, ID):
        self.tf_path = 'Backend/models/' + self.firstname + self.lastname + str(ID)


@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    user_dict = {
        "id":user.id,
        "firstname":user.firstname,
        "lastname":user.lastname,
        "tf_path":user.tf_path
    }
    return jsonify({"user" : user_dict})

@app.route('/api/v1/user', methods=['POST'])
def create_user():
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    user = User(firstname, lastname)
    db.session.add(user)
    db.session.commit()

    user.create_path(user.id)
    db.session.add(user)
    db.session.commit()

    return jsonify({"user_id":user.id})

@app.route('/api/v1/user', methods=['PUT'])
def update_user():
    ID = request.json["user_id"]
    user = User.query.filter_by(id=ID).first()
    user.num_dollars = request.json["num_dollars"]
    user.max_distance = request.json["max_distance"]
    user.fav_cuisine = request.json["fav_cuisine"]
    db.session.commit()
    return "", 200

@app.route('/api/v1/user', methods=['DELETE'])
def delete_user():
    ID = request.json["user_id"]
    user = User.query.filter_by(id=ID).first()
    db.session.delete(user)
    db.session.commit()
    return "", 200

@app.route('/api/v1/recommend', methods=['POST'])
def recommend():
    user_id = request.json["user_id"]
    user = User.query.get(user_id)

    latitude = 43.472285
    longitude = -80.544858
    cuisine = user.fav_cuisine
    num_dollars = user.num_dollars
    distance = str(user.distance)
    time = datetime.datetime.now()

    queries = {
        "lat":latitude,
        "lon":longitude,
        "cuisine":cuisine,
        "price":num_dollars,
        "time":time,
        "distance":distance
    }

    topThree = returnTopThree(user.tf_path, queries)
    return jsonify("array":topThree)


class Experience(db.Model):
    __tablename__ = "experiences"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float)
    logitude = db.Column(db.Float)
    restaurant = db.Column(db.String(200))
    num_dollars = db.Column(db.Integer)
    time_visited = db.Column(db.DateTime)
    rating = db.Column(db.Float)

    def __init__(self, user_id, latitude, logitude, restaurant, 
            num_dollars, time_visited, rating):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.restaurant = restaurant
        self.num_dollars = num_dollars
        self.time_visited = datetime.datetime.now() # DATE FORMAT???
        self.rating = rating

@app.route('/api/v1/experience', methods=['POST'])
def add_experience():
    user_id = request.json["user_id"]
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    restaurant = request.json["restaurant"]
    num_dollars = request.json["num_dollars"]
    time_visited = request.json["time_visited"]
    distance = request.json["distance"]

    # experience = Experience(user_id, latitude, longitude, restaurant,
    #         num_dollars, time_visited)
    # db.session.add(experience)
    # db.session.commit()

    # Pass data to zamato
    # Generate shifts of this data to train

@app.route('/')
def home():
    return "App Running"

if __name__ == '__main__':
    db.create_all()


    # s3 = boto3.resource('s3')
    # s3.Object(os.environ.get('S3_BUCKET'), 'BaseModel/BaseModel.txt').put(Body=open('models/BaseModel.txt', 'rb'))

    if os.environ.get("PORT") is None:
        app.run(debug=True, port=5000)
    else:
        app.run(debug=False, host='0.0.0.0', port=os.environ["PORT"])
