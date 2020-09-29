from .auth import LoginApi
from flask import request
from .admission import AdmissionListResource, AdmissionResource, GetSchools
from .resources import UserListResource, UserResource, StudentResource
from .login import UserLoginResource

def initialize_routes(api):
    api.add_resource(UserListResource, '/api')
    api.add_resource(UserResource, '/api/<int:req_id>')
    api.add_resource(StudentResource, '/api/search/<string:req_id>')
    api.add_resource(UserLoginResource, '/api/login')
    api.add_resource(AdmissionListResource, '/api/admission')
    api.add_resource(GetSchools, '/api/schools')
    api.add_resource(AdmissionResource, '/api/admission/<int:student_id>')