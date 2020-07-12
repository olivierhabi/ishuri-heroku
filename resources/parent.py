from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, Parent
from .model_super import db
from sqlalchemy import exc
from .model_super import parent_schema, parents_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime



class ParentListResource(Resource):
    @jwt_required
    def get(self):
        parent = Parent.query.all()
        return  parents_schema.dump(parent)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        admin = Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't Only Admin of school"
            }
            return error, 403

        try:
            body = request.get_json()
            role = "parent"
            new_parent = Parent(
                name = request.json['name'],
                email = request.json['email'],
                phone = request.json['phone'],
                password= generate_password_hash(request.json['password']).decode('utf8'),
                role = role,
                student_id = request.json['student_id'],
                school_id = admin.school_id
            )

            user = Parent.query.filter_by(email = body.get('email')).first()
            if user:
                errors = {
                    "status": 400,
                    "message": "Email was taken try another"
                }
                return errors, 400

            db.session.add(new_parent)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Parent created Successfully",
                "data": parent_schema.dump(new_parent)
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
        
        except TypeError:
            return {"status": 400, "message": " 'NoneType Error' Expected object got nothing" }, 400

class ParentResource(Resource):
    @jwt_required
    def get(self, parent_id):
        parent = Parent.query.get_or_404(parent_id)
        return parent_schema.dump(parent)

    @jwt_required
    def patch(self, parent_id):
        user_id = get_jwt_identity()
        admin =  Admin.query.get_or_404(user_id)
        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403
        
        try:
            body = request.get_json()

            parent = Parent.query.get_or_404(parent_id)

            if 'name' in request.json:
                parent.name = request.json['name']
            
            if 'student_id' in request.json:
                parent.student_id = request.json['student_id']

            if 'password' in request.json:
                if not 'current_password' in request.json:
                    errors_pass = {
                        "status": 400,
                        "message": "Missing Current Password"
                    }
                    return errors_pass, 400
                current_password = request.json['current_password']
                authorized = check_password_hash(parent.password, current_password)

                if not authorized:
                    errors_change = {
                        "status": 400,
                        "message": "Incorent Current Password"
                    }
                    return errors_change, 400

                parent.password = generate_password_hash(request.json['password']).decode('utf8'),

            

            db.session.commit()
            return parent_schema.dump(parent)

        except exc.IntegrityError:
            errors = {
                    "status": 400,
                    "message": "Invalid Foreign Key"
            }
            return errors, 400

    @jwt_required
    def delete(self, parent_id):
        user_id = get_jwt_identity()
        admin =  Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403

        parent = Parent.query.get_or_404(parent_id)
        db.session.delete(parent)
        db.session.commit()
        return '', 204

class ParentLogin(Resource):
    def post(self):
        try:
            body = request.get_json()
            password = body.get('password')
            user = Parent.query.filter_by(email = body.get('email')).first()
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

