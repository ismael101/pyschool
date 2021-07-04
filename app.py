from flask import Flask
from auth import auth
from file import file
from flask_marshmallow import Marshmallow 


# Init app
app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(file)

# basedir = os.path.abspath(os.path.dirname(__file__))

# # Init ma
# ma = Marshmallow(app)

# # Product Schema
# class FileSchema(ma.Schema):
#   class Meta:
#     fields = ('id', 'name',  'size', 'created')

# class UserSchema(ma.Schema):
#   class Meta:
#     fields = ('id', 'username',  'password')


# # Init schema
# file_schema = FileSchema()
# files_schema = FileSchema(many=True)
# user_schema = UserSchema()

# Run Server
if __name__ == '__main__':
  app.run(debug=True)