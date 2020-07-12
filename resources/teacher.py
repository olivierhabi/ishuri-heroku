from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, Teacher
from .model_super import db
from sqlalchemy import exc
from .model_super import teacher_schema, teachers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash


class TeacherListResource(Resource):
    @jwt_required
    def get(self):
        teacher = Teacher.query.all()
        return teachers_schema.dump(teacher)

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
                role = "teacher"
                new_teacher = Teacher(
                    email = request.json['email'],
                    password= generate_password_hash(request.json['password']).decode('utf8'),
                    phone = request.json['phone'],
                    role = role,
                    school_id = admin.school_id
                )

                user = Teacher.query.filter_by(email = body.get('email')).first()
                if user:
                    errors = {
                        "status": 400,
                        "message": "Email was taken try another"
                    }
                    return errors, 400

                db.session.add(new_teacher)
                db.session.commit()
                message = {
                    "status": 201,
                    "message": "Teacher created Successfully",
                    "data": teacher_schema.dump(new_teacher)
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
                "message": "Only Admin can create Teacher"
            }
            return errors, 400


class TeacherResource(Resource):

    @jwt_required
    def get(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        return teacher_schema.dump(teacher)
    
    @jwt_required
    def patch(self, teacher_id):
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
                teacher = Teacher.query.get_or_404(teacher_id)

                if 'email' in request.json:
                    teacher.email = request.json['email']

                if 'phone' in request.json:
                    teacher.phone = request.json['phone']

                if 'password' in request.json:
                    if not 'current_password' in request.json:
                        errors_pass = {
                            "status": 400,
                            "message": "Missing Current Password"
                        }
                        return errors_pass, 400
                    current_password = request.json['current_password']
                    authorized = check_password_hash(teacher.password, current_password)

                    if not authorized:
                        errors_change = {
                            "status": 400,
                            "message": "Incorent Current Password"
                        }
                        return errors_change, 400

                    teacher.password = generate_password_hash(request.json['password']).decode('utf8'),

                db.session.commit()
                return teacher_schema.dump(teacher)

            except exc.IntegrityError:
                errors = {
                    "status": 400,
                    "message": "Email already taken try another"
                }
                return errors, 400
        except:
            errors = {
                "status": 400,
                "message": "Only Admin can Update Teacher"
            }
            return errors, 400
    

    @jwt_required
    def delete(self, teacher_id):
        try:
            user_id = get_jwt_identity()
            admin =  Admin.query.get_or_404(user_id)
            if admin.role != "admin":
                error = {
                    "status": 403,
                    "message": "You can't you're not an admin"
                }
                return error, 403

            teacher = Teacher.query.get_or_404(teacher_id)
            db.session.delete(teacher)
            db.session.commit()
            return '', 204
        except:
            errors = {
                "status": 404,
                "message": "Content not found or You're Unauthorized"
            }
            return errors, 404


