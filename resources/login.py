from flask_restful import Api, Resource
from .model_super import Super, User
from flask import Flask, request
from .model_super import db
from flask_bcrypt import generate_password_hash, check_password_hash
from .model_super import super_schema, supers_schema, super_admin_schema, super_admins_schema, admin_schema, admins_schema, libralian_schema, libralians_schema, parent_schema, parents_schema 
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from sqlalchemy import exc
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime




class UserLoginResource(Resource):
    def post(self):
        try:
            request_header = request.headers["Request-Type"]
        
            if "login" in request_header:
                try:
                    body = request.get_json()
                    password = body.get('password')
                    user = User.query.filter_by(email = body.get('email')).first()
                    if not user:
                        errors = {
                            "status": 401,
                            "message": "Invalid Email or Password"
                        }
                        return errors, 401

                    if user.activation == 0:
                        errors = {
                            "status": 401,
                            "message": "Your Account is Deactivated contact your administrator"
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

                except AttributeError:
                    return {"status": 400, "message": "AttributeError Empty object Please fill required field" }, 400


            else:

                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                return errors, 400

        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Error Request-Type required " + str(e)
            }
            return errors, 400