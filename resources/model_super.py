from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
import datetime
import jsonpickle
from flask_cors import CORS
import os
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = str(consumer_key)
app.config['SQLALCHEMY_ECHO'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
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
    admin = db.relationship("User")
    classes = db.relationship("Classes")
    book = db.relationship("Book")
    activation = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default = datetime.datetime.strftime(datetime.datetime.today(), "%b %d %Y"))
    

    def __repr__(self):
        return '<School %s>' % self.name


class SchoolSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "phone", "bank_accounts", "location", "activation","created_date")


school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)


class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    academic_year = db.Column(db.String(1024))
    start_date = db.Column(db.String(1024))
    end_date = db.Column(db.String(1024))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Term %s>' % self.name


class TermSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "academic_year", "start_date","end_date", "school_id", "created_date")


term_schema = TermSchema()
terms_schema = TermSchema(many=True)





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





class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1280))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    
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
        fields = ("id", "name","ssn_number", "book_number", "school_id")


book_schema = BookSchema()
books_schema = BookSchema(many=True)



class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    email = db.Column(db.String(1024))
    password = db.Column(db.String(1024))
    id_number = db.Column(db.String(1024))
    birth_date = db.Column(db.String(1024))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<firstname %s>' % self.firstname


class AdmissionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name","email","birth_date", "password", "id_number", "school_id", "created_date")


admission_schema = AdmissionSchema()
admissions_schema = AdmissionSchema(many=True)

class AdmissionLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    ref_admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<name %s>' % self.name


class AdmissionLetterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "id_number", "birth_date", "school_id")


admission_letter_schema = AdmissionLetterSchema()
admission_letters_schema = AdmissionLetterSchema(many=True)

# 1: Student add (student card number)
# 2: Parent
# 3: Teacher
# 4: HeadTeacher
# 5: School Admin
# 6: Super User
# 7: Librarian

#ACTIVATION CODE

# 1: Activated
# 2: Deactivated


class User(db.Model):
    prefix = "USER"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(1024))
    role = db.Column(db.Integer)
    activation = db.Column(db.Integer)
    ref_student_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Reference for Parent
    ref_parent_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Reference for Student
    student_id = db.Column(db.String(15)) #generated_auto
    birth_date = db.Column(db.String(255))
    id_number = db.Column(db.String(1024))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    past_class = db.Column(db.Integer, db.ForeignKey('classes.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    created_date = db.Column(db.DateTime, default = datetime.datetime.strftime(datetime.datetime.today(), "%b %d %Y"))

    def __repr__(self):
        return '<User %s>' % self.name


class Userchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "phone", 'role' , 
        'ref_student_id','activation', 'ref_parent_id', 'student_id',
        'birth_date', 'class_id', 'past_class','id_number', 'school_id', 'created_date')


user_schema = Userchema()
users_schema = Userchema(many=True)

log_user_schema = Userchema(only=('id','role'))
log_users_schema = Userchema(many=True)

# super Admin
super_admin_schema = Userchema(only=('id','name', 'email','phone','role'))
super_admins_schema = Userchema(many=True)

# Admin
admin_schema = Userchema(only=('id','name', 'email','phone','school_id','role'))
admins_schema = Userchema(many=True)

# Librarian
libralian_schema = Userchema(only=('id','name', 'email','phone','school_id','role'))
libralians_schema = Userchema(many=True)

# Parent
parent_schema = Userchema(only=('id','name', 'email','phone','school_id','ref_student_id','role'))
parents_schema = Userchema(many=True)


# Teacher
teacher_schema = Userchema(only=('id','name', 'email','phone','school_id','role'))
teachers_schema = Userchema(many=True)

# HeadTeacher
head_teacher_schema = Userchema(only=('id','name', 'email','phone','school_id','role'))
head_teachers_schema = Userchema(many=True)

#Student
student_schema = Userchema(only=('id','name', 'email','birth_date','id_number','phone','school_id','role', 'student_id', 'created_date'))
students_schema = Userchema(many=True)
