from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import Admin, Super
from .model_super import db
from sqlalchemy import exc
from .model_super import admin_schema, admins_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime


class AdminListResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        super = []
        try:
            super =  Super.query.get_or_404(user_id)
        except:
            print("Something went wrong")
            super =  Admin.query.get_or_404(user_id)

        if super.role != "superadmin" and super.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        admin = Admin.query.all()
        return  admins_schema.dump(admin)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        super = []
        try:
            super =  Super.query.get_or_404(user_id)
        except:
            print("Something went wrong")
            super =  Admin.query.get_or_404(user_id)

        if super.role != "superadmin" and super.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        try:
            body = request.get_json()
            role = 'admin'
            new_admin = Admin(
                email = request.json['email'],
                password= generate_password_hash(request.json['password']).decode('utf8'),
                phone = request.json['phone'],
                role = role,
                school_id = request.json['school_id']
            )

            user = Admin.query.filter_by(email = body.get('email')).first()
            if user:
                errors = {
                    "status": 400,
                    "message": "Email was taken try another"
                }
                return errors, 400
            
            db.session.add(new_admin)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Admin created Successfully",
                "data": admin_schema.dump(new_admin)
                }
            return message, 201
        
        except exc.IntegrityError:
            errors = {
                "status": 400,
                "message": "Invalid Foreign Key"
            }
            return errors, 400
        
        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Request is missing required fields"
            }
            return errors, 400

class AdminResource(Resource):
    @jwt_required
    def get(self, admin_id):
        user_id = get_jwt_identity()
        super = []
        try:
            super =  Super.query.get_or_404(user_id)
        except:
            print("Something went wrong")
            super =  Admin.query.get_or_404(user_id)

        if super.role != "superadmin" and super.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403

        admin = Admin.query.get_or_404(admin_id)
        return admin_schema.dump(admin)
    @jwt_required
    def patch(self, admin_id):
        user_id = get_jwt_identity()
        super = []
        try:
            super =  Super.query.get_or_404(user_id)
        except:
            super =  Admin.query.get_or_404(user_id)

        if super.role != "superadmin" and super.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin or admin"
            }
            return error, 403
        try:
            admin= Admin.query.get_or_404(admin_id)

            if 'email' in request.json:
                admin.email = request.json['email']

            if 'phone' in request.json:
                admin.phone = request.json['phone']

            if 'password' in request.json:
                if not 'current_password' in request.json:
                    errors_pass = {
                        "status": 400,
                        "message": "Missing Current Password"
                    }
                    return errors_pass, 400
                current_password = request.json['current_password']
                authorized = check_password_hash(admin.password, current_password)

                if not authorized:
                    errors_change = {
                        "status": 400,
                        "message": "Incorent Current Password"
                    }
                    return errors_change, 400

                admin.password= generate_password_hash(request.json['password']).decode('utf8')

            db.session.commit()
            return admin_schema.dump(admin)

        except exc.IntegrityError:
            errors = {
                "status": 400,
                "message": "Email already taken try another"
            }
            return errors, 400
    @jwt_required
    def delete(self, admin_id):
        user_id = get_jwt_identity()
        super = []
        try:
            super =  Super.query.get_or_404(user_id)
        except:
            print("Something went wrong")
            super =  Admin.query.get_or_404(user_id)

        if super.role != "superadmin" and super.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        admin = Admin.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return '', 204

class AdminLogin(Resource):
    def post(self):
        try:
            body = request.get_json()
            password = body.get('password')
            user = Admin.query.filter_by(email = body.get('email')).first()
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

        except AttributeError:
            return {"status": 400, "message": "AttributeError Empty object Please fill required field" }, 400