from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView


from .. import db, bcrypt

from .models import User

auth_blueprint = Blueprint('auth', __name__,)

class RegisterAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(login=post_data.get('login')).first()
        if not user:
            try:
                hashed_password = bcrypt.generate_password_hash(post_data.get('password')).decode('utf-8')
                user = User(
                    login=post_data.get('login'),
                    password=hashed_password,
                    name=post_data.get('name'),
                    lastname=post_data.get('lastname'),
                    user_type=post_data.get('user_type'),
                    role_id=post_data.get('role_id')
                )

                db.session.add(user)
                db.session.commit()

                auth_token = user.encode_token(user.id, user.role_id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObject)), 202

class LoginAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            user = User.query.filter_by(login=post_data.get('login')).first()
            if user and bcrypt.check_password_hash(user.password, post_data.get('password')):
                auth_token = user.encode_token(user.id, user.role_id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Login failed. Username or password incorrect.'
                }
                return make_response(jsonify(responseObject)), 401
        except:
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
        
class LogoutAPI(MethodView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_token(auth_token)
            if not isinstance(resp, str):
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
        
class UserAPI(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'id': user.id,
                        'login': user.login,
                        'name': user.name,
                        'lastname': user.lastname,
                        'user_type': user.user_type,
                        'role_id': user.role_id
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        

register_view = RegisterAPI.as_view('register_api')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=register_view,
    methods=['POST']
)

login_view = LoginAPI.as_view('login_api')
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

logout_view = LogoutAPI.as_view('logout_api')
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

user_view = UserAPI.as_view('user_api')
auth_blueprint.add_url_rule(
    '/auth/user',
    view_func=user_view,
    methods=['GET']
)
