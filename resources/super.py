from flask_restful import Api, Resource
from .model_super import User, School, Term, Classes, Book, AdmissionLetter, Admission
from flask import Flask, request
from .model_super import db
from flask_bcrypt import generate_password_hash, check_password_hash
from .model_super import super_schema, supers_schema, super_admin_schema, super_admins_schema, user_schema,admin_schema, admins_schema, libralian_schema, libralians_schema, parent_schema, parents_schema, teacher_schema, teachers_schema, school_schema, head_teacher_schema, head_teachers_schema, term_schema, class_schema, book_schema, student_schema, schools_schema, terms_schema, classes_schema, books_schema, students_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from sqlalchemy import exc
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime





def post():
    email = "test@gmail.com"
    name = "test"
    phone = "078888888"
    password = "1234567890"


    try:
        role = 6
        new_super = User(
            name=name,
            email=email,
            phone=phone,
            password= generate_password_hash(password).decode('utf8'),
            role=role
        )

        user = User.query.filter_by(email = email).first()
        if user:
            errors = {
                "status": 400,
                "message": "Email was taken try another"
            }
            return errors, 400

        db.session.add(new_super)
        db.session.commit()
        message = {
            "status": 201,
            "message": "Super admin created Successfully",
            "data": user_schema.dump(new_super)
            }
        return message, 201
    
    except KeyError as e:
        errors = {
            "status": 400,
            "message": "Request is missing required fields " + str(e)
        }
        return errors, 400