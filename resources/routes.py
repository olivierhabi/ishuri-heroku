from .auth import LoginApi
from .super import SuperResource, SuperListResource
from .auth import LoginApi
from .school import SchoolListResource, SchoolResource
from .term import  TermListResource, TermResource
from .admin import AdminListResource, AdminResource, AdminLogin
from .libralian import LibralianListResource, LibralianResource, LoginLibrary
from .head_teacher import HeadTeacherResource, HeadTeacherListResource
from .teacher import TeacherListResource, TeacherResource
from .classes import ClassesListResource, ClassesResource
from .book import BookListResource, BookResource
from .student import StudentListResource, StudentResource, StudentLogin
from .parent import ParentListResource, ParentResource, ParentLogin
from .admission import AdmissionListResource, AdmissionResource
from .admission_letter import LetterListResource, LetterResource


def initialize_routes(api):
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(SuperListResource, '/api/super')
    api.add_resource(SuperResource, '/api/supers/<int:super_id>')

    api.add_resource(SchoolListResource, '/api/school')
    api.add_resource(SchoolResource, '/api/school/<int:school_id>')

    api.add_resource(TermListResource, '/api/term')
    api.add_resource(TermResource, '/api/term/<int:term_id>')

    api.add_resource(AdminListResource, '/api/admin')
    api.add_resource(AdminLogin, '/api/admin/login')
    api.add_resource(AdminResource, '/api/admin/<int:admin_id>')

    api.add_resource(LibralianListResource, '/api/libralian')
    api.add_resource(LibralianResource, '/api/libralian/<int:library_id>')
    api.add_resource(LoginLibrary, '/api/libralian/login')

    api.add_resource(HeadTeacherListResource, '/api/head')
    api.add_resource(HeadTeacherResource, '/api/head/<int:head_id>')
    
    api.add_resource(TeacherListResource, '/api/teacher')
    api.add_resource(TeacherResource, '/api/teacher/<int:teacher_id>')

    api.add_resource(ClassesListResource, '/api/class')
    api.add_resource(ClassesResource, '/api/class/<int:class_id>')

    api.add_resource(BookListResource, '/api/book')
    api.add_resource(BookResource, '/api/book/<int:book_id>')

    api.add_resource(StudentListResource, '/api/student')
    api.add_resource(StudentResource, '/api/student/<int:student_id>')
    api.add_resource(StudentLogin, '/api/student/login')

    api.add_resource(ParentListResource, '/api/parent')
    api.add_resource(ParentResource, '/api/parent/<int:parent_id>')
    api.add_resource(ParentLogin, '/api/parent/login')

    api.add_resource(AdmissionListResource, '/api/admission')
    api.add_resource(AdmissionResource, '/api/admission/<int:student_id>')

    api.add_resource(LetterListResource, '/api/letter')
    api.add_resource(LetterResource, '/api/letter/<int:letter_id>')