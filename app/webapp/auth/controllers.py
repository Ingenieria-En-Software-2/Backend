from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from flask import Response
from webapp.auth.token import *
from webapp.auth.email_verification import send_verification_email

auth_blueprint = Blueprint("auth", __name__)

from .. import db, bcrypt

from .models import User, Role


@auth_blueprint.route("/")
def login():
    return "I am a Login"


class RegisterAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(login=post_data.get("login")).first()
        if not user:
            try:
                hashed_password = bcrypt.generate_password_hash(
                    post_data.get("password")
                ).decode("utf-8")
                user = User(
                    login=post_data.get("login"),
                    password=hashed_password,
                    name=post_data.get("name"),
                    lastname=post_data.get("lastname"),
                    user_type=post_data.get("user_type"),
                    role_id=post_data.get("role_id"),
                )

                db.session.add(user)
                db.session.commit()

                ## To protect an EP to ensure that is a logged user use the decorator: @jwt_required(fresh=True)
                ## To get the value in the identity use the function: get_jwt_identity
                auth_token = create_access_token(
                    identity={"role": user.role_id, "user_id": user.id}, fresh=True
                )
                refresh_token = create_refresh_token(
                    identity={"role": user.role_id, "user_id": user.id}
                )

                responseObject = {
                    "status": "success",
                    "message": "Successfully registered.",
                    "auth_token": auth_token,
                    "refresh_token": refresh_token,
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    "status": "fail",
                    "message": "Some error occurred. Please try again.",
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "User already exists. Please Log in.",
            }
            return make_response(jsonify(responseObject)), 202


class RefreshAPI(MethodView):
    # If we are refreshing a token here we have not verified the users password in
    # a while, so mark the newly created access token as not fresh
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)


class LoginAPI(MethodView):
    def post(self):
        post_data = request.get_json()
        try:
            user = User.query.filter_by(login=post_data.get("login")).first()
            if (
                user
                and bcrypt.check_password_hash(user.password, post_data.get("password"))
                and user.verified == True
            ):
                ## To protect an EP to ensure that is a logged user use the decorator: @jwt_required(fresh=True)
                ## To get the value in the identity use the function: get_jwt_identity
                auth_token = create_access_token(
                    identity={"role": user.role_id, "user_id": user.id}, fresh=True
                )
                refresh_token = create_refresh_token(
                    identity={"role": user.role_id, "user_id": user.id}
                )

                if auth_token:
                    responseObject = {
                        "status": "success",
                        "message": "Successfully logged in.",
                        "auth_token": auth_token,
                        "refresh_token": refresh_token,
                    }
                return make_response(jsonify(responseObject)), 200
            elif user.verified == False:
                responseObject = {
                    "status": "fail",
                    "message": "Login failed. User not verified.",
                }

                # Send verification email again
                send_verification_email(user.login)

                return make_response(jsonify(responseObject)), 400
            else:
                responseObject = {
                    "status": "fail",
                    "message": "Login failed. Username or password incorrect.",
                }
                return make_response(jsonify(responseObject)), 401
        except:
            responseObject = {"status": "fail", "message": "Try again"}
            return make_response(jsonify(responseObject)), 500

    def options(self):
        resp = Response()
        resp.headers["Allow"] = "POST"
        return resp


class LogoutAPI(MethodView):
    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()

        if user_identity:
            resp = User.decode_token(user_identity)
            if not isinstance(resp, str):
                responseObject = {
                    "status": "success",
                    "message": "Successfully logged out.",
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {"status": "fail", "message": resp}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return make_response(jsonify(responseObject)), 403


class UserAPI(MethodView):
    @jwt_required(fresh=True)
    def get(self):
        user_identity = get_jwt_identity()

        if user_identity:
            resp = User.decode_token(user_identity)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                responseObject = {
                    "status": "success",
                    "data": {
                        "id": user.id,
                        "login": user.login,
                        "name": user.name,
                        "lastname": user.lastname,
                        "user_type": user.user_type,
                        "role_id": user.role_id,
                    },
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {"status": "fail", "message": resp}
            return make_response(jsonify(responseObject)), 401


class VerifyAPI(MethodView):
    # Como es una página que verá el usuario, no se retorna un JSON
    def get(self):
        token = request.args.get("token")
        if token:
            login = confirm_token(token)
            if login:
                user = User.query.filter_by(login=login).first()
                user.verified = True
                db.session.commit()

                return "Has verificado tu cuenta exitosamente, ahora puedes iniciar sesión"

        return "Verificacion fallida, intenta de nuevo"


register_view = RegisterAPI.as_view("register_api")
auth_blueprint.add_url_rule("/auth/register", view_func=register_view, methods=["POST"])

verify_view = VerifyAPI.as_view("verify_api")
auth_blueprint.add_url_rule("/auth/verify", view_func=verify_view, methods=["GET"])

login_view = LoginAPI.as_view("login_api")
auth_blueprint.add_url_rule(
    "/auth/login", view_func=login_view, methods=["POST", "OPTIONS"]
)

logout_view = LogoutAPI.as_view("logout_api")
auth_blueprint.add_url_rule("/auth/logout", view_func=logout_view, methods=["POST"])

user_view = UserAPI.as_view("user_api")
auth_blueprint.add_url_rule("/auth/user", view_func=user_view, methods=["GET"])

refresh_view = RefreshAPI.as_view("refresh_api")
auth_blueprint.add_url_rule("/auth/refresh", view_func=refresh_view, methods=["POST"])
