import json
from flask import Blueprint, request, jsonify
from flask_marshmallow import Marshmallow 
from sqlalchemy.exc import IntegrityError
from models import session, User, File
from auth import token_required
import os

file = Blueprint('file' ,__name__, url_prefix='/api')

@file.route('/upload', methods=['POST'])
@token_required
def upload(current_user):
    return jsonify(current_user.id)
    # if 'file' not in request.files:
    #     return jsonify({'error':'no file uploaded'}), 400
    # file = request.file['file']
    # user = session.query(User).filter_by(id=current_user).first()
    # os.path.join(f'/files/{user.id}/')
    # new_file = File(name=file.filename, size=file.filesize, type=file.mimetype, user_id=current_user)
    # session.add(new_file)
    # session.commit()
    # return jsonify('file uploaded successfully'), 201


