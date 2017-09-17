import os
import json

import boto3
from shutil import copyfile

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy




BaseModel = "Backend/models/BaseModel"

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
    ID = request.json["user"]["id"]
    user = User.query.filter_by(id=ID).first()
    user.firstname = request.json["user"]["firstname"]
    user.lastname = request.json["user"]["lastname"]
    user.create_path(user.id)
    db.session.commit()


    user_dict = {
        "id":user.id,
        "firstname":user.firstname,
        "lastname":user.lastname,
        "tf_path":user.tf_path
    }
    return jsonify({"user":user_dict})

@app.route('/api/v1/user', methods=['DELETE'])
def delete_user():
    ID = request.json["id"]
    user = User.query.filter_by(id=ID).first()
    db.session.delete(user)
    db.session.commit()
    return "", 200

@app.route('/api/v1/train', methods=['POST'])
def train():
    ID = request.json["id"]
    user = User.query.filter_by(id=ID).first()

    # function that takes in the path to model trained for that user,
    # and uses it to train using other queries.
    model = learning_models.train(user.tf_path)

@app.route('/')
def home():
    return "App Running"

if __name__ == '__main__':
    db.create_all()

    # train base model on startup

    # s3 = boto3.resource('s3')
    # s3.Object(os.environ.get('S3_BUCKET'), 'BaseModel/BaseModel.txt').put(Body=open('models/BaseModel.txt', 'rb'))

    if os.environ.get("PORT") is None:
        app.run(debug=True, port=5000)
    else:
        app.run(debug=False, host='0.0.0.0', port=os.environ["PORT"])
