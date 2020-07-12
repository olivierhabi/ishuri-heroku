from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import Super
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
import datetime


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        password = body.get('password')
        user = Super.query.filter_by(email = body.get('email')).first()
        if not user:
            errors = {
                "status": 401,
                "message": "Invalid Email or Password"
            }
            return errors, 401

        authorized = check_password_hash(user.password, password)

        if not authorized:
            errors = {
                "status": 401,
                "message": "Invalid Email or Password"
            }
            return errors, 401
        expires = datetime.timedelta(days=7)
       
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {"status": 200, "message": "Successfully logged in",'token': access_token}, 200
        