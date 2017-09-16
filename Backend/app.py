import os
import urlparse

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
if os.environ.get("DATABASE_URL") is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/food_recommendation'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    tf_path = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    user_dict = {
        "id":user.id,
        "name":user.name,
        "tf_path":user.tf_path
    }
    return jsonify({"user" : user_dict})

@app.route('/api/v1/user', methods=['POST'])
def create_user():
    name = request.json["name"]
    user = User(name)
    db.session.add(user)
    db.session.commit()

    user_dict = {
        "id":user.id,
        "name":user.name,
        "tf_path":user.tf_path
    }
    return jsonify({"user":user_dict})

@app.route('/api/v1/user', methods=['PUT'])
def update_user():
    ID = request.json["user"]["id"]
    user = User.query.filter_by(id=ID).first()
    user.name = request.json["user"]["name"]
    user.tf_path = request.json["user"]["tf_path"]
    db.session.commit()

    user_dict = {
        "id":user.id,
        "name":user.name,
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




@app.route('/')
def home():
    return "App Running"

if __name__ == '__main__':
    db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
