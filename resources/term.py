from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Super, Term
from .model_super import db
from sqlalchemy import exc
from .model_super import terms_schema, term_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


class TermListResource(Resource):
    
    def get(self):
        terms = Term.query.all()
        return  terms_schema.dump(terms)

    def post(self):
        try:
            new_term = Term(
                name =request.json['name'],
                days=request.json['days'],
                school_id= request.json['school_id']
            )
            
            db.session.add(new_term)
            db.session.commit()

            message = {
                "status": 201,
                "message": "Term created Successfully",
                "data": term_schema.dump(new_term)
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

class TermResource(Resource):
    def get(self, term_id):
        term = Term.query.get_or_404(term_id)
        return term_schema.dump(term)

    def patch(self, term_id):
        term = Term.query.get_or_404(term_id)

        if 'name' in request.json:
            term.name = request.json['name']

        if 'days' in request.json:
            term.days = request.json['days']

        if 'phone' in request.json:
            term.school_id = request.json['phone']

        db.session.commit()
        message = {
                "status": 200,
                "message": "Term Updated Successfully",
                "data": term_schema.dump(term)
                }
        return message, 200
    
    def delete(self, term_id):
        term = Term.query.get_or_404(term_id)
        db.session.delete(term)
        db.session.commit()
        return '', 204