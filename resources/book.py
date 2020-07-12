from flask_restful import Api, Resource
from flask import Flask, request
from .model_super import School, Admin, HeadTeacher, Book, Libralian
from .model_super import db
from sqlalchemy import exc
from .model_super import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash


class BookListResource(Resource):

    @jwt_required
    def get(self):
        book = Book.query.all()
        return books_schema.dump(book)

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            library = Libralian.query.get_or_404(user_id)

            if library.role != "library":
                error = {
                    "status": 403,
                    "message": "You can't Only Libralian"
                }
                return error, 403
            try:
                body = request.get_json()
                new_book = Book(
                    name = request.json['name'],
                    ssn_number= request.json['ssn_number'],
                    school_id = library.school_id,
                )

                db.session.add(new_book)
                db.session.commit()
                message = {
                    "status": 201,
                    "message": "Book created Successfully",
                    "data": book_schema.dump(new_book)
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
                "message": "Only Librarian can create book"
            }
            return errors, 400


class BookResource(Resource):

    @jwt_required
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    
    @jwt_required
    def patch(self, book_id):
        try:
            user_id = get_jwt_identity()
            library = Libralian.query.get_or_404(user_id)

            if library.role != "library":
                error = {
                    "status": 403,
                    "message": "You can't Only Libralian"
                }
                return error, 403

            book = Book.query.get_or_404(book_id)

            if 'name' in request.json:
                book.name = request.json['name']

            if 'ssn_number' in request.json:
                book.ssn_number = request.json['ssn_number']

            db.session.commit()
            return book_schema.dump(book)
        except:
            errors = {
                "status": 400,
                "message": "Only Librarian can Update book"
            }
            return errors, 400

    @jwt_required
    def delete(self, book_id):
        try:
            user_id = get_jwt_identity()
            library = Libralian.query.get_or_404(user_id)

            if library.role != "library":
                error = {
                    "status": 403,
                    "message": "You can't Only Libralian"
                }
                return error, 403

            book = Book.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
            return '', 204
        except:
            errors = {
                "status": 400,
                "message": "Content not found or You're Unauthorized"
            }
            return errors, 400
