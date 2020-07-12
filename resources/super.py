from flask_restful import Api, Resource
from .model_super import Super
from flask import Flask, request
from .model_super import db
from flask_bcrypt import generate_password_hash, check_password_hash
from .model_super import super_schema, supers_schema


class SuperListResource(Resource):
    def get(self):
        supers = Super.query.all()
        return supers_schema.dump(supers)

    def post(self):
        try:
            role = 'superadmin'
            new_super = Super(
                email=request.json['email'],
                phone=request.json['phone'],
                password= generate_password_hash(request.json['password']).decode('utf8'),
                role=role
            )

            db.session.add(new_super)
            db.session.commit()
            message = {
                "status": 201,
                "message": "Super admin created Successfully",
                "data": super_schema.dump(new_super)
                }
            return message, 201
        
        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Request is missing required fields"
            }
            return errors, 400


class SuperResource(Resource):
    def get(self, super_id):
        super = Super.query.get_or_404(super_id)
        return super_schema.dump(super)

    def patch(self, super_id):
        super= Super.query.get_or_404(super_id)

        if 'email' in request.json:
            super.email = request.json['email']

        if 'phone' in request.json:
            super.phone = request.json['phone']

        if 'current_password' in request.json:
            if request.json['current_password'] != super.password:
                errors = {
                "status": 400,
                "message": "Incorent Current Password"
                }
                return errors, 400

        if 'password' in request.json:
            super.password = request.json['password']
        
        if 'role' in request.json:
            super.role = request.json['role']

        db.session.commit()
        return super_schema.dump(super)

    def delete(self, super_id):
        super = Super.query.get_or_404(super_id)
        db.session.delete(super)
        db.session.commit()
        return '', 204