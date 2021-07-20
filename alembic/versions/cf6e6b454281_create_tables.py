"""create tables

Revision ID: cf6e6b454281
Revises: 
Create Date: 2021-07-20 03:55:22.877955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import bcrypt
import os

# revision identifiers, used by Alembic.
revision = 'cf6e6b454281'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    register = op.create_table('register',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('kind', postgresql.ENUM('ADMIN', 'TEACHER', 'STUDENT', name='level', create_type=False), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    users = op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('register_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['register_id'], ['register.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('register_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('credit', sa.Float(), nullable=False),
    sa.Column('teacher', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['teacher'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('modules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kind', postgresql.ENUM('HOMEWORK', 'QUIZ', 'PROJECT', 'TEST', name='type', create_type=False), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=255), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


    op.bulk_insert(register,[{'id':1, 'firstname':os.environ['FIRST'], 'lastname':os.environ['LAST'], 'email':os.environ['EMAIL'], 'kind':'ADMIN'}])
    op.bulk_insert(users, [{'id':1, 'username':os.environ['USERNAME'], 'password':bcrypt.hashpw(os.environ['PASSWORD'].encode('utf-8'), bcrypt.gensalt()), 'register_id':1}])

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('modules')
    op.drop_table('classlist')
    op.drop_table('classes')
    op.drop_table('users')
    op.drop_table('register')
    # ### end Alembic commands ###
