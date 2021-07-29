from flask import Blueprint, json, request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import Modules, Registery, session
from marshmallow import Schema, fields
from services.auth import token_required
from models import Role

modules = Blueprint('modules' ,__name__, url_prefix='/api')

class ModulesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    subject = fields.Str()
    credit = fields.Int()
    teacher = fields.Str()

moduleSchema = ModulesSchema()
moduleSchemas = ModulesSchema(many=True)


@modules.route('/modules/course/<id>', methods=['GET'])
def getModules(current_user, role, id):
    
    modules = session.query(Modules).filter_by(course=id)
    if modules.first() is None:
        return jsonify({'error':'modules dont exist'})
    return jsonify(moduleSchemas.dump(modules))

@modules.route('/modules/<id>', methods=['GET'])
def getModules(current_user, role, id):
    modules = session.query(Modules).filter_by(id=id)
    if modules.first() is None: 
        return jsonify({'error':'modules dont exist'})
    return jsonify(moduleSchemas.dump(modules))




