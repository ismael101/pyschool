# from services.auth import token_required
# from flask import Blueprint, request, jsonify
# from sqlalchemy.exc import IntegrityError
# from models import Register, session
# from marshmallow import Schema, fields

# register = Blueprint('register' ,__name__, url_prefix='/api')

# class RegisterSchema(Schema):
#     id = fields.Int()
#     first_name = fields.Str()
#     last_name = fields.Str()
#     email = fields.Str()
#     level = fields.Str()

# registerSchema = RegisterSchema(many=True)

# @register.route('/register', methods=['GET'])
# @token_required
# def getRegister(current_user, level):
#     if level == 'ADMIN':
#         register = session.query(Register).get()
#         return jsonify(registerSchema.dump(register)), 200
#     return jsonify({'error':'access denied'}), 401

# @register.route('/register/<id>', methods=['GET'])
# @token_required
# def getRegistered(current_user, level):
#     if level == 'ADMIN':
#         register = session.query(Register).get(request.id).first()
#         if register is None:
#             return jsonify({'error':"no register found"}), 400
#         return jsonify(registerSchema.dump(register)), 200
#     else:
#         return jsonify({'error':'access denied'}), 401

# @register.route('/register', methods=['POST'])
# @token_required
# def createRegister(current_user, level):
#     try:
#         if level == 'ADMIN':
#             new_register = Register(first_name=request.first_name, last_name=request.last_name, email=request.email, level=request.level)
#             session.add(new_register)
#             session.commit()
#             return jsonify({'error':'new register created'}), 201
#         return jsonify({'error':'unauthorized request'}), 401 
#     except IntegrityError:
#         return jsonify({'error':'register already exists'}), 400




