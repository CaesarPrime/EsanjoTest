from flask import Flask, request
import urllib.request
import requests, json
# import mysql.connector as mysql
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                            as Serializer, BadSignature, SignatureExpired)
import pymysql
import task1

try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'toor'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://esanjo:toor@localhost/esanjo_test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

@app.route('/')
def index():
    return 'Assignment by - Pasan Chamikara'

#Task1
@app.route('/task1')
def assignment1():
    response =  requests.get('https://res.cloudinary.com/esanjolabs/raw/upload/v1529967088/tests/categories-test.json')
    # json_data = json.load(response.content)
    data = response.json()
    flat_inst = task1.Flatten()
    flat_inst.flat(data, 10)
    lst = flat_inst.returnList()

    # for i in lst:
    #     print(i)
    print(len(lst))

    lst = sorted(lst, key=lambda k: k['objectId']) 
    x = json.dumps(lst)
    return x

#Task 2
@app.route('/task2')
@auth.login_required
def assignment2():
    page = request.args.get('page', default = 1, type=int)
    records = request.args.get('records', default=10 , type=int)

    if page is not None or records is not None:
        start_at = (page - 1)* records
        end_at = start_at + records

        results = Pagination_Details.query.offset(start_at).limit(end_at).all()
        # print(results)
        lst = {}
        dct = []
        for i in results:
            lst['id'] = i.id
            lst['name'] = i.name
            lst['description'] = i.description
            dct.append(lst)
            lst = {}

        # result_dict = [r for r, in results]
        return json.dumps(dct)

    return 'task2'

class Pagination_Details(db.Model):
    __tablename__ = 'pagination_sample'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String(50))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55), index=True)
    password_hash = db.Column(db.String(255))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


# @app.route('/api/resource')
# @auth.login_required
# def get_resource():
#     return jsonify({'data': 'Hello, %s!' % g.user.username})

@app.errorhandler(404)
def page_not_found(e):
    return "Page Not Found"

if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    # db.create_all()
    app.run(debug=True)