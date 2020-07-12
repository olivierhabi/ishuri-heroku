from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, HeadTeacher
from .model_super import db
from sqlalchemy import exc
from .model_super import head_teacher_schema, head_teachers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash



class HeadTeacherListResource(Resource):
    def get(self):
        head_teacher = HeadTeacher.query.all()
        return head_teachers_schema.dump(head_teacher)

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
                role = "head_teacher"
                new_head_teacher = HeadTeacher(
                    email = request.json['email'],
                    password= generate_password_hash(request.json['password']).decode('utf8'),
                    phone = request.json['phone'],
                    role = role,
                    school_id = admin.school_id
                )

                user = HeadTeacher.query.filter_by(email = body.get('email')).first()
                if user:
                    errors = {
                        "status": 400,
                        "message": "Email was taken try another"
                    }
                    return errors, 400

                db.session.add(new_head_teacher)
                db.session.commit()
                message = {
                    "status": 201,
                    "message": "Head Teacher created Successfully",
                    "data": head_teacher_schema.dump(new_head_teacher)
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
                "message": "Only Admin can create Head Teacher"
            }
            return errors, 400

class HeadTeacherResource(Resource):

    @jwt_required
    def get(self, head_id):
        head_teacher = HeadTeacher.query.get_or_404(head_id)
        return head_teacher_schema.dump(head_teacher)

    @jwt_required
    def patch(self, head_id):
        try:
            user_id = get_jwt_identity()
            admin =  Admin.query.get_or_404(user_id)
            if admin.role != "admin":
                error = {
                    "status": 403,
                    "message": "You can't you're not an admin"
                }
                return error, 403

            try:
                head_teacher = HeadTeacher.query.get_or_404(head_id)

                if 'email' in request.json:
                    head_teacher.email = request.json['email']

                if 'phone' in request.json:
                    head_teacher.phone = request.json['phone']

                if 'password' in request.json:
                    if not 'current_password' in request.json:
                        errors_pass = {
                            "status": 400,
                            "message": "Missing Current Password"
                        }
                        return errors_pass, 400
                    current_password = request.json['current_password']
                    authorized = check_password_hash(head_teacher.password, current_password)

                    if not authorized:
                        errors_change = {
                            "status": 400,
                            "message": "Incorent Current Password"
                        }
                        return errors_change, 400

                    head_teacher.password = generate_password_hash(request.json['password']).decode('utf8'),

                db.session.commit()
                return head_teacher_schema.dump(head_teacher)

            except exc.IntegrityError:
                errors = {
                    "status": 400,
                    "message": "Email already taken try another"
                }
                return errors, 400
        except:
            errors = {
                "status": 400,
                "message": "Only Admin can Update Head Teacher"
            }
            return errors, 400

    @jwt_required
    def delete(self, head_id):
        try:
            user_id = get_jwt_identity()
            admin =  Admin.query.get_or_404(user_id)
            if admin.role != "admin":
                error = {
                    "status": 403,
                    "message": "You can't you're not an admin"
                }
                return error, 403

            head_teacher = HeadTeacher.query.get_or_404(head_id)
            db.session.delete(head_teacher)
            db.session.commit()
            return '', 204
        except:
            errors = {
                "status": 400,
                "message": "Content not found or You're Unauthorized"
            }
            return errors, 400
