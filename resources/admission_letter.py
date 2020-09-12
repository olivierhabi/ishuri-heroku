from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, AdmissionLetter
from .model_super import db
from sqlalchemy import exc
from .model_super import admission_letter_schema, admission_letters_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
  


class LetterListResource(Resource):
    @jwt_required
    def get(self):
        letters = AdmissionLetter.query.all()
        return  admission_letters_schema.dump(letters)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()['id']
        admin = Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't Only Admin of school"
            }
            return error, 403

        try:
            body = request.get_json()
            new_letter = AdmissionLetter(
                letter = request.json['letter'],
                student_id = request.json['student_id'],
                school_id = admin.school_id
            )

            db.session.add(new_letter)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Admission Letter created Successfully",
                "data": admission_letter_schema.dump(new_letter)
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


class LetterResource(Resource):
    @jwt_required
    def get(self, letter_id):
        letter = AdmissionLetter.query.get_or_404(letter_id)
        return admission_letter_schema.dump(letter)

    @jwt_required
    def patch(self, letter_id):
        user_id = get_jwt_identity()['id']
        admin =  Admin.query.get_or_404(user_id)
        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403
        
        try:
            body = request.get_json()

            letter = AdmissionLetter.query.get_or_404(letter_id)

            if 'letter' in request.json:
                letter.letter = request.json['letter']
            
            if 'student_id' in request.json:
                letter.student_id = request.json['student_id']

            db.session.commit()
            return admission_letter_schema.dump(letter)

        except exc.IntegrityError:
            errors = {
                    "status": 400,
                    "message": "Invalid Foreign Key"
            }
            return errors, 400

    @jwt_required
    def delete(self, letter_id):
        user_id = get_jwt_identity()['id']
        admin =  Admin.query.get_or_404(user_id)

        if admin.role != "admin":
            error = {
                "status": 403,
                "message": "You can't you're not an admin"
            }
            return error, 403

        letter = AdmissionLetter.query.get_or_404(letter_id)
        db.session.delete(letter)
        db.session.commit()
        return '', 204
