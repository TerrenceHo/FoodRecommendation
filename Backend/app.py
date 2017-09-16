from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/food_recommendation'
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
    return jsonify({"id":user.id})

@app.route('/api/v1/user', methods=['DELETE'])
def delete_user():
    ID = request.json["id"]
    user = User.query.filter_by(id=ID).first()
    db.session.delete(user)
    db.session.commit()
    return "", 200





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
