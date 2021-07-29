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

class Role(enum.Enum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

class Module(enum.Enum):
    HOMEWORK = 'HOMEWORK'
    QUIZ = 'QUIZ'
    PROJECT = 'PROJECT'
    TEST = 'TEST'

class Subject(enum.Enum):
    MATH = 'MATH'
    LANGUAGE = 'LANGUAGE'
    SCIENCE = 'SCIENCE'
    TECHNOLOGY = 'TECHNOLOGY'
    ENGINEERING = 'ENGINEERING'
    HUMANITIES = 'HUMANITIES'

class Registery(Base):
    __tablename__ = 'registery'
    id = Column(Integer, primary_key=True)
    first = Column(String(255), nullable=False)
    last = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(ENUM(Role), nullable=False)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    register = Column(Integer, ForeignKey('registery.id', ondelete='CASCADE'), nullable=False, unique=True)

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    subject = Column(ENUM(Subject), nullable=False) 
    credit = Column(Integer, nullable=False)
    teacher = Column(Integer, ForeignKey('registery.id'), nullable=False)

class Classlist(Base):
    __tablename__ = 'classlist'
    id = Column(Integer, primary_key=True)
    course =  Column(Integer, ForeignKey('course.id', ondelete='CASCADE'))
    student = Column(Integer, ForeignKey('registery.id', ondelete='CASCADE'))

class Modules(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    module = Column(ENUM(Module), nullable=False)  
    course = Column(Integer, ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(String(255), nullable=False)  
    module = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    student = Column(Integer, ForeignKey('registery.id', ondelete='CASCADE'), nullable=False)

engine = create_engine(os.environ['DB'], echo=False)
Session = sessionmaker(bind=engine)
session = Session()