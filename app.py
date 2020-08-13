from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
import datetime
import jsonpickle
import os
from dotenv import load_dotenv
from resources.super import post


# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('SQLALCHEMY_DATABASE_URI')
secret_key = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  str(consumer_key)
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = str(secret_key)
jwt = JWTManager(app)

@app.before_request
def before_request_func():
    post()

from resources.routes import initialize_routes


# initialize_db(app)
initialize_routes(api)
if __name__ == '__main__':
    app.run(debug=True)