from flask_restful import Api, Resource
from .model_super import User, School, Term, Classes, Book, AdmissionLetter, Admission
from flask import Flask, request
from .model_super import db
from flask_bcrypt import generate_password_hash, check_password_hash
from .model_super import super_schema, supers_schema, super_admin_schema, super_admins_schema, user_schema,admin_schema, admins_schema, libralian_schema, libralians_schema, parent_schema, parents_schema, teacher_schema, teachers_schema, school_schema, head_teacher_schema, head_teachers_schema, term_schema, class_schema, book_schema, student_schema, schools_schema, terms_schema, classes_schema, books_schema, students_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from sqlalchemy import exc,  extract
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime



#superuser
#admin
#libralian
#parent
#teacher
#HeadTeacher

  


class UserListResource(Resource):
    @jwt_required
    def get(self):
        try:
            request_header = request.headers["Request-Type"]
            

            if "parent" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401

                parent = User.query.all()
                return  parents_schema.dump(parent)

            if "student" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401


                students = User.query.filter(User.school_id == super.school_id).filter(User.role == 1).all()

                return  students_schema.dump(students)


            if "book" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401

                book = Book.query.all()
                return books_schema.dump(book)


            if "class" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401

                classes = Classes.query.all()
                return classes_schema.dump(classes)


            if "no_teacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401

                teacher = User.query.all()
                return teachers_schema.dump(teacher)
                
            elif "headteacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401

                head_teacher = User.query.all()
                return head_teachers_schema.dump(head_teacher)



            elif "libralian" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401



                libralians = User.query.all()
                return  libralians_schema.dump(libralians)

            elif "admin" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither admin nor superadmin"
                    }
                    return error, 403


                admin = User.query.all()
                return  admins_schema.dump(admin)


            elif "superuser" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                
                if super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not superadmin"
                    }
                    return error, 403
                

                supers = User.query.all()
                return super_admins_schema.dump(supers)
            elif "school" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not superadmin"
                    }
                    return error, 403
                

                schools = School.query.all()
                return  schools_schema.dump(schools)
            elif "term" in request_header:
                terms = Term.query.all()
                return  terms_schema.dump(terms)
            else:
                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                return errors, 400


        except KeyError as e:
                errors = {
                    "status": 400,
                    "message": "Error Request-Type required " + str(e)
                }
                return errors, 
        except:
            session.rollback()


    @jwt_required
    def post(self):
        try:
            request_header = request.headers["Request-Type"]
        
        
            if "superuser" in request_header:
                try:
                    role = 6
                    new_super = User(
                        name=request.json['name'],
                        email=request.json['email'],
                        phone=request.json['phone'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        role=role
                    )

                    user = User.query.filter_by(email = request.json['email']).first()
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
                        "data": super_admin_schema.dump(new_super)
                        }
                    return message, 201
                
                except KeyError as e:
                    errors = {
                        "status": 400,
                        "message": "Request is missing required fields " + str(e)
                    }
                    return errors, 400
                except:
                    session.rollback()
                    raise

            
            elif "admin" in request_header:
                user_id = get_jwt_identity()['id']
                super =  User.query.get_or_404(user_id)

                

                if super.role != 6 and super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                try:
                    body = request.get_json()
                    role = 5
                    new_admin = User(
                        name=request.json['name'],
                        email = request.json['email'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        phone = request.json['phone'],
                        role = role,
                        school_id = request.json['school_id']
                    )

                    user = User.query.filter_by(email = body.get('email')).first()
                    if user:
                        errors = {
                            "status": 400,
                            "message": "Email was taken try another"
                        }
                        return errors, 400
                    
                    db.session.add(new_admin)
                    db.session.commit()
                    message = {
                        "status": 201,
                        "message": "Admin created Successfully",
                        "data":  admin_schema.dump(new_admin)
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
                except:
                    session.rollback()
                    raise

            elif "libralian" in request_header:
                user_id = get_jwt_identity()['id']
                super =  User.query.get_or_404(user_id)

                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 401,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 401


                try:
                    body = request.get_json()
                    role = 7
                    new_libralian = User(
                        name = request.json['name'],
                        email = request.json['email'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        phone = request.json['phone'],
                        role = role,
                        school_id = super.school_id
                    )

                    user = User.query.filter_by(email = body.get('email')).first()
                    if user:
                        errors = {
                            "status": 400,
                            "message": "Email was taken try another"
                        }
                        return errors, 400

                    db.session.add(new_libralian)
                    db.session.commit()
                    message = {
                        "status": 201,
                        "message": "Libralian created Successfully",
                        "data": libralian_schema.dump(new_libralian)
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
                except:
                    session.rollback()
                    raise

            elif "parent" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)

                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403
                
                try:
                    body = request.get_json()
                    role = 5
                    new_parent = User(
                        name = request.json['name'],
                        email = request.json['email'],
                        phone = request.json['phone'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        role = role,
                        ref_student_id = request.json['ref_student_id'],
                        school_id = admin.school_id
                    )

                    user = User.query.filter_by(email = body.get('email')).first()
                    if user:
                        errors = {
                            "status": 400,
                            "message": "Email was taken try another"
                        }
                        return errors, 400

                    db.session.add(new_parent)
                    db.session.commit()
                    message = {
                        "status": 201,
                        "message": "Parent created Successfully",
                        "data": parent_schema.dump(new_parent)
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
            
            
                except:
                    session.rollback()
                    raise

            elif "no_teacher" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)

                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    body = request.get_json()
                    role = 3
                    new_teacher = User(
                        name = request.json['name'],
                        email = request.json['email'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        phone = request.json['phone'],
                        role = role,
                        school_id = admin.school_id
                    )

                    user = User.query.filter_by(email = body.get('email')).first()
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
                        "message": "Request is missing required fields" + str(e)
                    }
                    return errors, 400
                except:
                    session.rollback()
                    raise

            elif "headteacher" in request_header:
                try:
                    user_id = get_jwt_identity()['id']
                    admin =  User.query.get_or_404(user_id)

                    if admin.role != 5:
                        error = {
                            "status": 403,
                            "message": "You can't you're not Admin"
                        }
                        return error, 403
                    
                    school = School.query.get_or_404(admin.school_id)
                    if school.activation == 0:
                        errors = {
                            "status": 403,
                            "message": "Action Blocked contact your administrator"
                        }
                        return errors, 403
                    try:
                        body = request.get_json()
                        role = 4
                        new_head_teacher = User(
                            name = request.json['name'],
                            email = request.json['email'],
                            password= generate_password_hash(request.json['password']).decode('utf8'),
                            phone = request.json['phone'],
                            role = role,
                            school_id = admin.school_id
                        )

                        user = User.query.filter_by(email = body.get('email')).first()
                        if user:
                            errors = {
                                "status": 400,
                                "message": "Email was taken try another"
                            }
                            return errors, 400

                        db.session.add(new_head_teacher)
                        db.session.commit()
                        message = {
                            "status": 201,
                            "message": "Head Teacher created Successfully",
                            "data": head_teacher_schema.dump(new_head_teacher)
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

                    except:
                        session.rollback()
                        raise
                    

                except:
                    errors = {
                        "status": 400,
                        "message": "Only Admin can create Head Teacher"
                    }
                    return errors, 400
                
                
            elif "school" in request_header:
                user_id = get_jwt_identity()['id']

                super = User.query.get_or_404(user_id)
                if super.role != 6:
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
                        "message": "Request is missing required fields " + str(e)
                    }
                    return errors, 400

                except:
                    session.rollback()
                    raise

            elif "term" in request_header:
                try:
                    user_id = get_jwt_identity()['id']
                    admin = User.query.get_or_404(user_id)

                    if admin.role != 5:
                        error = {
                            "status": 403,
                            "message": "You can't Only Admin of school"
                        }
                        return error, 403
                    
                    school = School.query.get_or_404(admin.school_id)
                    if school.activation == 0:
                        errors = {
                            "status": 403,
                            "message": "Action Blocked contact your administrator"
                        }
                        return errors, 403
                    
                    try:
                        new_term = Term(
                            name =request.json['name'],
                            academic_year =request.json['academic_year'],
                            start_date =request.json['start_date'],
                            end_date =request.json['end_date'],
                            school_id= admin.school_id
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
                            "message": "Request is missing required fields " + str(e)
                        }
                        return errors, 400
                    except:
                        session.rollback()
                        raise
                except:
                    errors = {
                        "status": 400,
                        "message": "Only Admin can create Term"
                    }
                    return errors, 400

            elif "class" in request_header:
                try:
                    user_id = get_jwt_identity()['id']
                    admin = User.query.get_or_404(user_id)

                    if admin.role != 5:
                        error = {
                            "status": 403,
                            "message": "You can't Only Admin of school"
                        }
                        return error, 403
                    
                    school = School.query.get_or_404(admin.school_id)
                    if school.activation == 0:
                        errors = {
                            "status": 403,
                            "message": "Action Blocked contact your administrator"
                        }
                        return errors, 403

                    try:
                        body = request.get_json()
                        new_class = Classes(
                            name = request.json['name'],
                            school_id = admin.school_id
                        )

                        db.session.add(new_class)
                        db.session.commit()
                        message = {
                            "status": 201,
                            "message": "Class created Successfully",
                            "data": class_schema.dump(new_class)
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
                        session.rollback()
                        raise

                except:
                    errors = {
                        "status": 400,
                        "message": "Only Admin can create Class"
                    }
                    return errors, 400

            elif "book" in request_header:
                try:
                    user_id = get_jwt_identity()['id']
                    library = User.query.get_or_404(user_id)

                    if library.role != 7:
                        error = {
                            "status": 403,
                            "message": "You can't Only Libralian"
                        }
                        return error, 403
                    
                    school = School.query.get_or_404(library.school_id)
                    if school.activation == 0:
                        errors = {
                            "status": 403,
                            "message": "Action Blocked contact your administrator"
                        }
                        return errors, 403

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
                        session.rollback()
                        raise

                except:
                    errors = {
                        "status": 400,
                        "message": "Only Librarian can create book"
                    }
                    return errors, 400

            if "student" in request_header:
                user_id = get_jwt_identity()['id']
                admin = User.query.get_or_404(user_id)

                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't Only Admin of school"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    body = request.get_json()
                    role = 1
                    student_id = 2020

                    todays_datetime = datetime.datetime(datetime.datetime.today().year,  datetime.datetime.today().month, datetime.datetime.today().day)
                    students = User.query.filter(User.school_id == admin.school_id).filter(User.role == 1).filter(extract('year', User.created_date) == todays_datetime.year).all()

                    student_number_gen = students.__len__() + 1
                    pk_id = str(student_number_gen).zfill(5)

                    school = School.query.get_or_404(admin.school_id)
                    school_name = school.name

                    words = school_name.split()
                    letters = [word[0] for word in words]
                    short_school = "".join(letters).upper()

                    student_id = str(todays_datetime.year) + str(short_school) + pk_id


                    new_student = User(
                        name = request.json['name'],
                        email = request.json['email'],
                        phone = request.json['phone'],
                        password= generate_password_hash(request.json['password']).decode('utf8'),
                        role = role,
                        student_id = student_id,
                        birth_date = request.json['birth_date'],
                        id_number = request.json['id_number'],
                        class_id = request.json['class_id'],
                        school_id = admin.school_id
                    )

                    user = User.query.filter_by(email = body.get('email')).first()
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
                        "message": "Request is missing required fields " + str(e)
                    }
                    return errors, 400
                
                except TypeError:
                    return {"status": 400, "message": " 'NoneType Error' Expected object got nothing" }, 400

                except:
                    session.rollback()
                    raise
        
            else:

                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                return errors, 400

        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Error Request-Type required " + str(e)
            }
            return errors, 400





class UserResource(Resource):
    @jwt_required
    def get(self, req_id):
        try:
            request_header = request.headers["Request-Type"]

            if "parent" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403

                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                parent = User.query.get_or_404(req_id)
                return parent_schema.dump(parent)

            if "student" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                student = User.query.get_or_404(req_id)
                return student_schema.dump(student)


            if "book" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 7:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Librarian"
                    }
                    return error, 403

                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                book = Book.query.get_or_404(req_id)
                return book_schema.dump(book)


            if "class" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                classes = Classes.query.get_or_404(req_id)
                return class_schema.dump(classes)

            if "no_teacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                teacher = User.query.get_or_404(req_id)
                return teacher_schema.dump(teacher)

            if "libralian" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                library = User.query.get_or_404(req_id)
                return libralian_schema.dump(library)

            elif "superuser" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not SuperAdmin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                super = User.query.get_or_404(req_id)
                return super_schema.dump(super)
            elif "school" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403
                    
                school = School.query.get_or_404(req_id)
                return school_schema.dump(school)\

            elif "term" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403
                    

                term = Term.query.get_or_404(req_id)
                return term_schema.dump(term)

            elif "admin" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither admin nor superadmin"
                    }
                    return error, 403
                
                


                admin = User.query.get_or_404(req_id)
                return admin_schema.dump(admin)

            elif "headteacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                head_teacher = User.query.get_or_404(req_id)
                return head_teacher_schema.dump(head_teacher)

            else:
                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                return errors, 400


        except KeyError as e:
                errors = {
                    "status": 400,
                    "message": "Error Request-Type required " + str(e)
                }
                return errors, 400

    @jwt_required
    def patch(self, req_id):
        try:
            request_header = request.headers["Request-Type"]

            if "parent" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403
                try:
                    body = request.get_json()

                    parent = User.query.get_or_404(req_id)

                    if 'name' in request.json:
                        parent.name = request.json['name']
                    
                    if 'student_id' in request.json:
                        parent.student_id = request.json['student_id']

                    if 'password' in request.json:
                        if not 'current_password' in request.json:
                            errors_pass = {
                                "status": 400,
                                "message": "Missing Current Password"
                            }
                            return errors_pass, 400
                        current_password = request.json['current_password']
                        authorized = check_password_hash(parent.password, current_password)

                        if not authorized:
                            errors_change = {
                                "status": 400,
                                "message": "Incorent Current Password"
                            }
                            return errors_change, 400

                        parent.password = generate_password_hash(request.json['password']).decode('utf8'),

                    

                    db.session.commit()
                    return parent_schema.dump(parent)

                except exc.IntegrityError:
                    errors = {
                            "status": 400,
                            "message": "Invalid Foreign Key"
                    }
                    return errors, 400

                except:
                    session.rollback()
                    raise


            if "student" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    body = request.get_json()

                    student = User.query.get_or_404(req_id)

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
                
                except:
                    session.rollback()
                    raise


            if "book" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 7:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Libralian"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                book = Book.query.get_or_404(req_id)

                if 'name' in request.json:
                    book.name = request.json['name']

                if 'ssn_number' in request.json:
                    book.ssn_number = request.json['ssn_number']

                db.session.commit()
                return book_schema.dump(book)

            if "class" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 3:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither Admin nor Teacher"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                classes = Classes.query.get_or_404(req_id)

                if 'name' in request.json:
                    classes.name = request.json['name']

                db.session.commit()
                return class_schema.dump(classes)

            if "no_teacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 3:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither Admin nor Teacher"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    teacher = User.query.get_or_404(req_id)

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
                    session.rollback()
                    raise

            if "headteacher" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    head_teacher = User.query.get_or_404(req_id)

                    if 'email' in request.json:
                        head_teacher.email = request.json['email']

                    if 'phone' in request.json:
                        head_teacher.phone = request.json['phone']

                    if 'password' in request.json:
                        if not 'current_password' in request.json:
                            errors_pass = {
                                "status": 400,
                                "message": "Missing Current Password"
                            }
                            return errors_pass, 400
                        current_password = request.json['current_password']
                        authorized = check_password_hash(head_teacher.password, current_password)

                        if not authorized:
                            errors_change = {
                                "status": 400,
                                "message": "Incorent Current Password"
                            }
                            return errors_change, 400

                        head_teacher.password = generate_password_hash(request.json['password']).decode('utf8'),

                    db.session.commit()
                    return head_teacher_schema.dump(head_teacher)

                except exc.IntegrityError:
                    errors = {
                        "status": 400,
                        "message": "Email already taken try another"
                    }
                    return errors, 400

                except:
                    session.rollback()
                    raise

            if "libralian" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 7:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither admin nor libralian"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    library = User.query.get_or_404(req_id)

                    if 'email' in request.json:
                        library.email = request.json['email']

                    if 'phone' in request.json:
                        library.phone = request.json['phone']

                    if 'password' in request.json:
                        if not 'current_password' in request.json:
                            errors_pass = {
                                "status": 400,
                                "message": "Missing Current Password"
                            }
                            return errors_pass, 400
                        current_password = request.json['current_password']
                        authorized = check_password_hash(library.password, current_password)

                        if not authorized:
                            errors_change = {
                                "status": 400,
                                "message": "Incorent Current Password"
                            }
                            return errors_change, 400

                        library.password = generate_password_hash(request.json['password']).decode('utf8'),

                    db.session.commit()
                    return libralian_schema.dump(library)

                except exc.IntegrityError:
                    errors = {
                        "status": 400,
                        "message": "Email already taken try another"
                    }
                    return errors, 400

                except:
                    session.rollback()
                    raise


            if "admin" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5 and super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're neither admin nor superadmin"
                    }
                    return error, 403
                
               

                try:
                    admin= User.query.get_or_404(req_id)

                    if 'email' in request.json:
                        admin.email = request.json['email']

                    if 'phone' in request.json:
                        admin.phone = request.json['phone']

                    if 'password' in request.json:
                        if not 'current_password' in request.json:
                            errors_pass = {
                                "status": 400,
                                "message": "Missing Current Password"
                            }
                            return errors_pass, 400
                        current_password = request.json['current_password']
                        authorized = check_password_hash(admin.password, current_password)

                        if not authorized:
                            errors_change = {
                                "status": 400,
                                "message": "Incorent Current Password"
                            }
                            return errors_change, 400

                        admin.password= generate_password_hash(request.json['password']).decode('utf8')

                    db.session.commit()
                    return admin_schema.dump(admin)

                except exc.IntegrityError:
                    errors = {
                        "status": 400,
                        "message": "Email already taken try another"
                    }
                    return errors, 400

                except:
                    session.rollback()
                    raise

            if "term" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(super.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403



                term = Term.query.get_or_404(req_id)

                if 'name' in request.json:
                    term.name = request.json['name']

                if 'academic_year' in request.json:
                    term.start_date = request.json['academic_year']

                if 'start_date' in request.json:
                    term.start_date = request.json['start_date']
                if 'end_date' in request.json:
                    term.end_date = request.json['end_date']

                db.session.commit()
                message = {
                        "status": 200,
                        "message": "Term Updated Successfully",
                        "data": term_schema.dump(term)
                        }
                return message, 200


            if "superuser" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)

                if super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not superadmin"
                    }
                    return error, 403
                

                super= User.query.get_or_404(req_id)

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

            if "school" in request_header:
                user_id = get_jwt_identity()['id']
                super = User.query.get_or_404(user_id)
                if super.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not superadmin"
                    }
                    return error, 403
                    

                school = School.query.get_or_404(req_id)

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

            
            else:
                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                return errors, 400


        except KeyError as e:
                errors = {
                    "status": 400,
                    "message": "Error Request-Type required " + str(e)
                }
                return errors, 400
    @jwt_required
    def post(self, req_id):
        try:
            request_header = request.headers["Request-Type"]

            if "admission" in request_header:
            
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)
                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not an admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403

                try:
                    admission = Admission.query.get_or_404(req_id)
                    


                    new_letter = AdmissionLetter(
                        body = request.json['body'],
                        class_id = request.json['class_id'],
                        ref_admission_id = admission.id,
                        school_id = admin.school_id
                    )

                    db.session.add(new_letter)
                    db.session.commit()

                    role = 1

                    todays_datetime = datetime.datetime(datetime.datetime.today().year,  datetime.datetime.today().month, datetime.datetime.today().day)
                    students = User.query.filter(User.school_id == admission.school_id).filter(User.role == 1).filter(extract('year', User.created_date) == todays_datetime.year).all()

                    student_number_gen = students.__len__() + 1
                    pk_id = str(student_number_gen).zfill(5)

                    school = School.query.get_or_404(admin.school_id)
                    school_name = school.name

                    words = school_name.split()
                    letters = [word[0] for word in words]
                    short_school = "".join(letters).upper()

                    student_id = str(todays_datetime.year) + str(short_school) + pk_id

                    

                    new_student = User(
                        name = admission.name,
                        email = admission.email,
                        password= admission.password,
                        role = role,
                        student_id = student_id,
                        birth_date = admission.birth_date,
                        id_number = admission.school_id,
                        class_id = request.json['class_id'],
                        school_id = admission.school_id,
                    )

                    db.session.add(new_student)
                    db.session.commit()
                    message = {
                        "status": 201,
                        "message": "Student created Successfully",
                        "data": student_schema.dump(new_student)
                        }
                    return message, 201


                    

                except KeyError as e:
                    errors = {
                        "status": 400,
                        "message": "Request is missing required fields " + str(e)
                    }
                    return errors, 400
                    
                except:
                    message = {
                        "status": 201,
                        "message": "Student is already registered"
                        }

                    return message, 
                
            
            if "activation" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)
                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not an admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                user =  User.query.get_or_404(req_id)
                user.activation = 1
                db.session.commit()
                return user_schema.dump(user)
            


            if "de_activate" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)
                if admin.role != 5:
                    error = {
                        "status": 403,
                        "message": "You can't you're not an admin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                user =  User.query.get_or_404(req_id)
                user.activation = 0
                db.session.commit()
                return user_schema.dump(user)
            

            if "sch_activa" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)
                if admin.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Superadmin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                school =  School.query.get_or_404(req_id)
                school.activation = 1
                db.session.commit()
                return school_schema.dump(school)

            

            if "deact_school" in request_header:
                user_id = get_jwt_identity()['id']
                admin =  User.query.get_or_404(user_id)
                if admin.role != 6:
                    error = {
                        "status": 403,
                        "message": "You can't you're not Superadmin"
                    }
                    return error, 403
                
                school = School.query.get_or_404(admin.school_id)
                if school.activation == 0:
                    errors = {
                        "status": 403,
                        "message": "Action Blocked contact your administrator"
                    }
                    return errors, 403


                school =  School.query.get_or_404(req_id)
                school.activation = 0
                db.session.commit()
                return school_schema.dump(school)
            
            else:
                errors = {
                    "status": 400,
                    "message": "Request type not found"
                }
                
                return errors, 400

        except KeyError as e:
            errors = {
                "status": 400,
                "message": "Error Request-Type required " + str(e)
            }
            return errors, 400
            
        except:
            session.rollback()
            raise



class StudentResource(Resource):
    @jwt_required
    def get(self, req_id):
        user_id = get_jwt_identity()['id']
        super = User.query.get_or_404(user_id)
        if super.role != 5:
            error = {
                "status": 403,
                "message": "You can't you're not Admin"
            }
            return error, 403
        
        school = School.query.get_or_404(admin.school_id)
        if school.activation == 0:
            errors = {
                "status": 403,
                "message": "Action Blocked contact your administrator"
            }
            return errors, 403

        student = User.query.filter_by(student_id = req_id ).first()
        return student_schema.dump(student)


        