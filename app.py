from flask import Flask
from services.auth import auth
from services.register import register


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(register)

if __name__ == '__main__':
  app.run(debug=True)