from flask import Blueprint, json, request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import Course, Registery, session
from marshmallow import Schema, fields
from services.auth import token_required
from models import Role

course = Blueprint('course' ,__name__, url_prefix='/api')

class CourseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    subject = fields.Str()
    credit = fields.Int()
    teacher = fields.Str()

courseSchema = CourseSchema()
courseSchemas = CourseSchema(many=True)

@course.route('/course', methods=['GET'])
@token_required
def getCourese(current_user, role):
    courses = session.query(Course).filter_by(id=id)
    if courses.first() is None:
        return jsonify({'error':'register entry doesnt exist'}), 400
    for c in courses.all():
        c.teacher = f'{session.query(Registery).filter_by(id=c.id).first().first} {session.query(Registery).filter_by(id=c.id).first().last}'
    return jsonify(courseSchemas.dump(courses)), 200

@course.route('/course/<id>', methods=['GET'])
@token_required
def getCourse(current_user, role, id):
    course = session.query(Course).filter_by(id=id).first()
    if course is None:
        return jsonify({'error':'register entry doesnt exist'}), 400
    course.teacher = f'{session.query(Registery).filter_by(id=course.id).first().first} {session.query(Registery).filter_by(id=course.id).first().last}'
    return jsonify(courseSchema.dump(course)), 200

@course.route('/course', methods=['POST'])
@token_required
def createCourse(current_user, role):
    try:
        if role == Role.ADMIN:
            new_course = Course(request.json)
            session.add(new_course)
            session.commit()
            return jsonify('new course created'), 201
        return jsonify({'error':'unauthorized action'}), 401
    except IntegrityError as i:
        session.rollback()
        return jsonify({'error':'course title already exists'}), 400
    except KeyError as k:
        session.rollback()
        return jsonify({'error':'incomplete response'}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error':'bad request'}), 400

@course.route('/course/<id>', methods=['PUT'])
@token_required
def updateCourse(current_user, role, id):
    try:
        if role == Role.ADMIN:
            course = session.query(Course).filter_by(id=id).first()
            if course is None:
                return jsonify({'error':'register entry doesnt exist'}), 400
            session.query(Course).filter_by(id=id).update(request.json)
            session.commit()
        return jsonify({'error':'unauthorized action'}), 401
    except IntegrityError:
        session.rollback()
        return jsonify({'error':'course title already exist'}), 400
    except Exception:
        session.rollback()
        return jsonify({'error':'bad request'}), 400

@course.route('/course/<id>', methods=['DELETE'])
@token_required
def deleteCourse(current_user, role, id):
    if role == Role.ADMIN:
        course = session.query(Course).filter_by(id=id).first()
        if course is None:
            return jsonify({'error':'course doesnt exist'}), 400
        session.query(Course).filter_by(id=id).delete()
        session.commit()
        return jsonify('course succesfully deleted'), 200
    return jsonify({'error':'unauthorized action'}), 401
