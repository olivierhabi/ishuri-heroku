from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin,  Student
from .model_super import db
from sqlalchemy import exc
from .model_super import student_schema, students_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime


class StudentListResource(Resource):
    @jwt_required
    def get(self):
        students = Student.query.all()
        return  students_schema.dump(students)

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
            role = "student"
            new_student = Student(
                name = request.json['name'],
                email = request.json['email'],
                password= generate_password_hash(request.json['password']).decode('utf8'),
                role = role,
                class_id = request.json['class_id'],
                school_id = admin.school_id
            )

            user = Student.query.filter_by(email = body.get('email')).first()
            if user:
                errors = {
                    "status": 400,
                    "message": "Email was taken try another"
                }
                return errors, 400

            db.session.add(new_student)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Student created Successfully",
                "data": student_schema.dump(new_student)
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


class StudentResource(Resource):
    @jwt_required
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student_schema.dump(student)

    @jwt_required
    def patch(self, student_id):
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

            student = Student.query.get_or_404(student_id)

            if 'name' in request.json:
                student.name = request.json['name']
            
            if 'class_id' in request.json:
                student.class_id = request.json['class_id']

            if 'password' in request.json:
                if not 'current_password' in request.json:
                    errors_pass = {
                        "status": 400,
                        "message": "Missing Current Password"
                    }
                    return errors_pass, 400
                current_password = request.json['current_password']
                authorized = check_password_hash(student.password, current_password)

                if not authorized:
                    errors_change = {
                        "status": 400,
                        "message": "Incorent Current Password"
                    }
                    return errors_change, 400

                student.password = generate_password_hash(request.json['password']).decode('utf8'),

            

            db.session.commit()
            return student_schema.dump(student)

        except exc.IntegrityError:
            errors = {
                    "status": 400,
                    "message": "Invalid Foreign Key"
            }
            return errors, 400


    @jwt_required
    def delete(self, student_id):
        user_id = get_jwt_identity()
        admin =  Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403

        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return '', 204


class StudentLogin(Resource):
    def post(self):
        try:
            body = request.get_json()
            password = body.get('password')
            user = Student.query.filter_by(email = body.get('email')).first()
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