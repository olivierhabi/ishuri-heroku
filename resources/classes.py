from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, Classes
from .model_super import db
from sqlalchemy import exc
from .model_super import class_schema, classes_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash


class ClassesListResource(Resource):

    @jwt_required
    def get(self):
        classes = Classes.query.all()
        return classes_schema.dump(classes)

    @jwt_required
    def post(self):
        try:
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
                new_class = Classes(
                    name = request.json['name'],
                    school_id = admin.school_id
                )

                db.session.add(new_class)
                db.session.commit()
                message = {
                    "status": 201,
                    "message": "Class created Successfully",
                    "data": class_schema.dump(new_class)
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

        except:
            errors = {
                "status": 400,
                "message": "Only Admin can create Class"
            }
            return errors, 400

class ClassesResource(Resource):

    @jwt_required
    def get(self, class_id):
        classes = Classes.query.get_or_404(class_id)
        return class_schema.dump(classes)

    @jwt_required
    def patch(self, class_id):
        user_id = get_jwt_identity()
        admin =  Admin.query.get_or_404(user_id)
        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403

        classes = Classes.query.get_or_404(class_id)

        if 'name' in request.json:
            classes.name = request.json['name']

        db.session.commit()
        return class_schema.dump(classes)

    @jwt_required
    def delete(self, class_id):
        try:
            user_id = get_jwt_identity()
            admin =  Admin.query.get_or_404(user_id)
            if admin.role != "admin":
                error = {
                    "status": 403,
                    "message": "You can't you're not an admin"
                }
                return error, 403

            classes = Classes.query.get_or_404(class_id)
            db.session.delete(classes)
            db.session.commit()
            return '', 204
        except:
            errors = {
                "status": 400,
                "message": "Content not found or You're Unauthorized"
            }
            return errors, 400

