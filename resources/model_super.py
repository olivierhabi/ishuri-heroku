from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
import datetime
import jsonpickle
import os
from dotenv import load_dotenv
#...

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = str(consumer_key)
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'Ishuri_Secret'
jwt = JWTManager(app)

class Super(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    

    def __repr__(self):
        return '<Super %s>' % self.email


class SuperSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phone", "role")


super_schema = SuperSchema()
supers_schema = SuperSchema(many=True)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1024))
    phone = db.Column(db.String(255))
    bank_accounts = db.Column(db.String(1280))
    location = db.Column(db.String(1280))
    term = db.relationship("Term")
    admin = db.relationship("Admin")
    libralian = db.relationship("Libralian")
    head_teacher = db.relationship("HeadTeacher")
    teacher = db.relationship("Teacher")
    classes = db.relationship("Classes")
    book = db.relationship("Book")
    

    def __repr__(self):
        return '<School %s>' % self.name


class SchoolSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "phone", "bank_accounts", "location")


school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)


class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    days = db.Column(db.String(1024))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Term %s>' % self.name


class TermSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "days", "school_id", "created_date")


term_schema = TermSchema()
terms_schema = TermSchema(many=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Admin %s>' % self.email


class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phone", "role", "school_id")


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class Libralian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Libralian %s>' % self.email


class LibralianSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phone", "role", "school_id")


libralian_schema = LibralianSchema()
libralians_schema = LibralianSchema(many=True)



class HeadTeacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<HeadTeacher %s>' % self.email


class HeadTeacherSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phone", "role", "school_id")


head_teacher_schema = HeadTeacherSchema()
head_teachers_schema = HeadTeacherSchema(many=True)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Teacher %s>' % self.email


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phone", "role", "school_id")


teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1280))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    student = db.relationship("Student")
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Classes %s>' % self.name


class ClassesSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "school_id")


class_schema = ClassesSchema()
classes_schema = ClassesSchema(many=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ssn_number = db.Column(db.String(255))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Book %s>' % self.name


class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "book_number", "school_id")


book_schema = BookSchema()
books_schema = BookSchema(many=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    parent = db.relationship("Parent")
    admission = db.relationship("Admission")
    role = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Student %s>' % self.name


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "class_id", "school_id")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    role = db.Column(db.String(50))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Student %s>' % self.name


class ParentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "phone", "student_id", "school_id")


parent_schema = ParentSchema()
parents_schema = ParentSchema(many=True)

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admited = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<student_id %s>' % self.student_id


class AdmissionSchema(ma.Schema):
    class Meta:
        fields = ("id", "admited", "student_id", "school_id")


admission_schema = AdmissionSchema()
admissions_schema = AdmissionSchema(many=True)

class AdmissionLetter(db.Model):
    payment_key = db.Column(db.Integer, db.Sequence('payment_seq'), unique=True, primary_key=True)
    letter = db.Column(db.String(50))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<payment_key %s>' % self.payment_key


class AdmissionLetterSchema(ma.Schema):
    class Meta:
        fields = ("id", "payment_key", "admited", "letter", "student_id", "school_id")


admission_letter_schema = AdmissionLetterSchema()
admission_letters_schema = AdmissionLetterSchema(many=True)

