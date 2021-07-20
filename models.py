from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import enum
import os

Base = declarative_base()
metadata = Base.metadata

class Level(enum.Enum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

class Type(enum.Enum):
    HOMEWORK = 'HOMEWORK'
    QUIZ = 'QUIZ'
    PROJECT = 'PROJECT'
    TEST = 'TEST'

class Register(Base):
    __tablename__ = 'register'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    kind = Column(ENUM(Level), nullable=False)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    register_id = Column(Integer, ForeignKey('register.id', ondelete='CASCADE'), nullable=False, unique=True)

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    credit = Column(Float, nullable=False)
    teacher = Column(Integer, ForeignKey('users.id'), nullable=False)

class Classlist(Base):
    __tablename__ = 'classlist'
    id = Column(Integer, primary_key=True)
    class_id =  Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

class Modules(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    kind = Column(ENUM(Type), nullable=False)  
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)

class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(String(255), nullable=False)  
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

engine = create_engine(os.environ['DB'], echo=False)
Session = sessionmaker(bind=engine)
session = Session()