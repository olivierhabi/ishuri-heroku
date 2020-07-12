from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, Admission
from .model_super import db
from sqlalchemy import exc
from .model_super import admission_schema, admissions_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

class AdmissionListResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        admin = Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't Only Admin of school"
            }
            return error, 403
            
        admission = Admission.query.all()
        return  admissions_schema.dump(admission)
    
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
            new_admission = Admission(
                admited = request.json['admited'],
                student_id = request.json['student_id'],
                school_id = admin.school_id
            )

            student = Admission.query.filter_by(student_id = body.get('student_id')).first()
            if student:
                errors = {
                    "status": 400,
                    "message": "You are created admission for this student try update instead"
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

        except exc.StatementError:
            errors = {
                "status": 400,
                "message": "'admited' Not a boolean value: 'true' or 'false'"
            }
            return errors, 400
        
        except KeyError:
            errors = {
                "status": 400,
                "message": "Request is missing required fields"
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

            admission = Admission.query.get_or_404(student_id)

            if 'admited' in request.json:
                admission.admited = request.json['admited']
            
            db.session.commit()
            return admission_schema.dump(admission)

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

        admission = Admission.query.get_or_404(student_id)
        db.session.delete(admission)
        db.session.commit()
        return '', 204

