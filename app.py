from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import User, File, session
from flask_marshmallow import Marshmallow 
import bcrypt
import jwt
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Init ma
ma = Marshmallow(app)

# Product Schema
class FileSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name',  'size', 'created')

class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username',  'password')


# Init schema
file_schema = FileSchema()
files_schema = FileSchema(many=True)
user_schema = UserSchema()


@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        username = request.json['username']
        password = request.json['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        session.add(new_user)
        session.commit()
        return jsonify('user succesfully created'), 201
    except IntegrityError:
        return jsonify({'error':'user already exists'}), 401

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    user = session.query(User).filter_by(username=username).first() 
    if user is not None:
        password = request.json['password']
        hashed_password = user.password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token = jwt.encode({'id': user.id.hex}, os.environ['SECRET'], algorithm='HS256')
            return jsonify({'token':token}), 201
        else:
            return jsonify({'error':'password incorrect'}), 401
    else:
        return jsonify('error', 'user doesnt exist'), 404

# Run Server
if __name__ == '__main__':
  app.run(debug=True)