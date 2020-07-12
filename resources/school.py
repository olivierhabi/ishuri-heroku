from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Super
from .model_super import db
from .model_super import school_schema, schools_schema
from flask_jwt_extended import jwt_required, get_jwt_identity



class SchoolListResource(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        super = Super.query.get_or_404(user_id)
        if super.role != "superadmin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403

        schools = School.query.all()
        return  schools_schema.dump(schools)
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        super = Super.query.get_or_404(user_id)
        if super.role != "superadmin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        try:
            new_school = School(
                name =request.json['name'],
                description=request.json['description'],
                phone= request.json['phone'],
                bank_accounts=request.json['bank_accounts'],
                location=request.json['location']
            )
            
            db.session.add(new_school)
            db.session.commit()
            message = {
                "status": 201,
                "message": "School created Successfully",
                "data": school_schema.dump(new_school)
                }
            return message, 201
        
        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Request is missing required fields"
            }
            return errors, 400

class SchoolResource(Resource):
    @jwt_required
    def get(self, school_id):
        user_id = get_jwt_identity()
        super = Super.query.get_or_404(user_id)
        if super.role != "superadmin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        school = School.query.get_or_404(school_id)
        return school_schema.dump(school)

    @jwt_required
    def patch(self, school_id):
        user_id = get_jwt_identity()
        super = Super.query.get_or_404(user_id)
        if super.role != "superadmin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403

        school = School.query.get_or_404(school_id)

        if 'name' in request.json:
            school.name = request.json['name']

        if 'description' in request.json:
            school.description = request.json['description']

        if 'phone' in request.json:
            school.phone = request.json['phone']

        
        if 'bank_accounts' in request.json:
            school.bank_accounts = request.json['bank_accounts']

        if 'location' in request.json:
            school.location = request.json['location']

        db.session.commit()
        message = {
                "status": 200,
                "message": "School Updated Successfully",
                "data": school_schema.dump(school)
                }
        return message, 200

    @jwt_required
    def delete(self, school_id):
        user_id = get_jwt_identity()
        super = Super.query.get_or_404(user_id)
        if super.role != "superadmin":
            error = {
                "status": 403,
                "message": "You can't you're not superadmin"
            }
            return error, 403
        school = School.query.get_or_404(school_id)
        db.session.delete(school)
        db.session.commit()
        return '', 204


