from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

@app.route('/api/v1/user/create', methods=['POST'])
def create_user():
    user = request.json["user"]
    # send data to database
    # retrieve data from database
    return jsonify({"test":user})

@app.route('/api/v1/user/delete', methods=['DEL'])
def delete_user():
    ID = request.json["id"]
    # validate delete user
    # delete user from firebase
    return _, 200



if __name__ == '__main__':
    app.run(debug=True)
