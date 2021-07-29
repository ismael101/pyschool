from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Registery, session
from marshmallow import Schema, fields
from services.auth import token_required
from models import Role

register = Blueprint('register' ,__name__, url_prefix='/api')

class RegisterSchema(Schema):
    id = fields.Int()
    firstname = fields.Str()
    lastname = fields.Str()
    email = fields.Str()
    role = fields.Str()

registerSchema = RegisterSchema()
registerSchemas = RegisterSchema(many=True)

@register.route('/register', methods=['GET'])
@token_required
def getRegister(current_user, role):
    if role == Role.ADMIN:
        register = session.query(Registery)
        return jsonify(registerSchemas.dump(register)), 200
    return jsonify({'error':'unauthorized access'}), 401

@register.route('/register/<id>', methods=['GET'])
@token_required
def getRegisterById(current_user, role, id):
    if role == Role.ADMIN:
        register = session.query(Registery).filter_by(id=id).first()
        if register is None:
            return jsonify({'error':'register entry doesnt exist'}), 400
        return jsonify(registerSchema.dump(register)), 200
    return jsonify({'error':'unauthorized access'}), 401

@register.route('/register', methods=['POST'])
@token_required
def createRegister(current_user, role):
    try:
        if role == Role.ADMIN:
            new_register = Registery(request.json)
            session.add(new_register)
            session.commit()
            return jsonify('new register created'), 201
        return jsonify({'error':'unauthorized action'}), 401
    except IntegrityError as i:
        session.rollback()
        return jsonify({'error':'register email already exists'}), 400
    except KeyError as k:
        session.rollback()
        return jsonify({'error':'incomplete response'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error':'bad request'}), 400

@register.route('/register/<id>', methods=['PUT'])
@token_required
def updateRegister(current_user, role, id):
    try:
        if role == Role.ADMIN:
            register = session.query(Registery).filter_by(id=id).first()
            if register is None:
                return jsonify({'error':'register doesnt exist'}), 400
            session.query(Registery).filter_by(id=id).update(request.json)
            session.commit()
        return jsonify({'error':'unauthorized action'}), 401
    except IntegrityError:
        session.rollback()
        return jsonify({'error':'register email already exist'}), 400
    except Exception:
        session.rollback()
        return jsonify({'error':'bad request'}), 400

@register.route('/register/<id>', methods=['DELETE'])
@token_required
def deleteRegister(current_user, role, id):
    if role == Role.ADMIN:
        register = session.query(Registery).filter_by(id=id).first()
        if register is None:
            return jsonify({'error':'register doesnt exist'}), 400
        session.query(Registery).filter_by(id=id).delete()
        session.commit()
        return jsonify('register succesfully deleted'), 200
    return jsonify({'error':'unauthorized action'}), 401
