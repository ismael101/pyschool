from flask import Flask
import bcrypt
import os
from services.auth import auth


app = Flask(__name__)
app.register_blueprint(auth)

if __name__ == '__main__':
  app.run(debug=True)