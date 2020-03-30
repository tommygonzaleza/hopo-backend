from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)


# Init ma
ma = Marshmallow(app)


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)

    def __init__(self, name, lastname, email, phone_number):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'lastname', 'email', 'phone_number')


# Init Schema
# It launches an error if u¡you use a marshmallow version older than 2.20.1
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


# Create an User
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    lastname = request.json['lastname']
    email = request.json['email']
    phone_number = request.json['phone_number']

    new_user = User(name, lastname, email, phone_number)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Get Single Users
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Get All Users
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# Update an User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    lastname = request.json['lastname']
    email = request.json['email']
    phone_number = request.json['phone_number']

    user.name = name
    user.lastname = lastname
    user.email = email
    user.phone_number = phone_number

    db.session.commit()

    return user_schema.jsonify(user)


# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    
    return user_schema.jsonify(user)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)


# To create de Database you need to:
# 1.- Write in the console: python
# 2.- Write in the console: from app import db
# 3.- Write in the console: db.create_all()