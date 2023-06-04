from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/")
def login():
    ## TODO: This should have logged user info and be on the post method for login
    ## To protect an EP to ensure that is a logged user use the decorator: @jwt_required(fresh=True)
    ## To get the value in the identity use the function: get_jwt_identity
    access_token = create_access_token(identity={"role": "admin", "user_id": 1}, fresh=True)
    refresh_token = create_refresh_token(identity={"role": "admin", "user_id": 1})
    return jsonify({ "token": access_token, "refresh_token": refresh_token})

# If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)