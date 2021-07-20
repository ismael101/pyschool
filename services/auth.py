from flask import Blueprint, request, jsonify
import datetime
from sqlalchemy.exc import IntegrityError
from models import Users, Register, session
from functools import wraps
import bcrypt
import jwt
import os

auth = Blueprint('auth' ,__name__, url_prefix='/api')
basedir = os.path.abspath(os.path.dirname(__file__))

@auth.route('/signup', methods=['POST'])
def signup():
    try:
        first_name = request.json['first_name']
        last_name  = request.json['last_name']
        email = request.json['email']
        registered_user = session.query(Register).filter_by(first_name=first_name, last_name=last_name, email=email).first()
        if registered_user is not None:
            username = request.json['username']
            password = request.json['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = Users(username=username, password=hashed_password.decode('utf-8'))
            session.add(new_user)
            session.commit()
            return jsonify('user succesfully created'), 201
        return jsonify({'error':'user isnt registered'}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error':'user already exists'}), 401

@auth.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    user = session.query(Users).filter_by(username=username).first() 
    if user is not None:
        password = request.json['password']
        hashed_password = user.password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token = jwt.encode({'id': f'{user.id}',"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, os.environ['SECRET'], algorithm='HS256')
            return jsonify({'token':token}), 201
        else:
            return jsonify({'error':'password incorrect'}), 401
    else:
        return jsonify({'error':'user doesnt exist'}), 400

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer[7:]
        if not token:
            return jsonify({'error' : 'token missing'}), 401
        try:
            data = jwt.decode(token, os.environ['SECRET'], algorithms=["HS256"])
            current_user = session.query(Users).get(data['id'])
            level = session.query(Register).get(current_user.register_id)
            if current_user is None:
                return jsonify({'error':'user doesnt exist'}), 400
        except:
            return jsonify({'error' : 'token invalid'}), 401
        return  f(current_user, level, *args, **kwargs)
    return decorated