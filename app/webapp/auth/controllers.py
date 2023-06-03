from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/")
def login():
    access_token = create_access_token(identity={"role": "admin", "user_id": 1})
    return jsonify({ "token": access_token})