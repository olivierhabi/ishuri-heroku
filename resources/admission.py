from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, User, Admission
from .model_super import db
from sqlalchemy import exc
from .model_super import admission_schema, admissions_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class AdmissionListResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()['id']
        admin = User.query.get_or_404(user_id)

        if admin.role != 5:
            error = {
                "status": 403,
                "message": "You can't Only Admin of school"
            }
            return error, 403
            
        admission = Admission.query.all()
        return  admissions_schema.dump(admission)
    
    
    def post(self):
        try:
            body = request.get_json()
            new_admission = Admission(
                name = request.json['name'],
                email = request.json['email'],
                id_number = request.json['id_number'],
                birth_date = request.json['birth_date'],
                password= generate_password_hash(request.json['password']).decode('utf8'),
                school_id = request.json['school_id']
            )

            user = Admission.query.filter_by(email = body.get('email')).first()
            if user:
                errors = {
                    "status": 400,
                    "message": "Email was taken try another"
                }
                return errors, 400

            db.session.add(new_admission)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Admission created Successfully",
                "data": admission_schema.dump(new_admission)
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
                "message": "Request is missing required fields " + str(e)
            }
            return errors, 400

        except TypeError:
            return {"status": 400, "message": " 'NoneType Error' Expected object got nothing" }, 400

class AdmissionResource(Resource):
    @jwt_required
    def get(self, student_id):
        admission = Admission.query.get_or_404(student_id)
        return admission_schema.dump(admission)

    @jwt_required
    def patch(self, student_id):
        user_id = get_jwt_identity()['id']
        admin =  User.query.get_or_404(user_id)
        if admin.role != 5:
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403
        
        try:
            body = request.get_json()

            admission = Admission.query.get_or_404(student_id)

            if 'firstname' in request.json:
                admission.firstname = request.json['firstname']
            if 'lastname' in request.json:
                admission.lastname = request.json['lastname']
            if 'email' in request.json:
                admission.email = request.json['email']
            if 'location' in request.json:
                admission.location = request.json['location']
            if 'school_id' in request.json:
                admission.school_id = request.json['school_id']
            
            if 'password' in request.json:
                if not 'current_password' in request.json:
                    errors_pass = {
                        "status": 400,
                        "message": "Missing Current Password"
                    }
                    return errors_pass, 400
                current_password = request.json['current_password']
                authorized = check_password_hash(admission.password, current_password)

                if not authorized:
                    errors_change = {
                        "status": 400,
                        "message": "Incorent Current Password"
                    }
                    return errors_change, 400

                admission.password= generate_password_hash(request.json['password']).decode('utf8')

                
            
            
            db.session.commit()
            return admission_schema.dump(admission)

        except exc.IntegrityError:
            errors = {
                    "status": 400,
                    "message": "Invalid Foreign Key"
            }
            return errors, 400

