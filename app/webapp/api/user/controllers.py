"""
Module containing the definition of the UserApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to users.
"""

from flask_restful import fields as fs
from ... import db
from ...auth.UserRepository import UserRepository
from ..generic.CrudApi import CrudApi
from .schemas import Create_User_Schema, Update_User_Schema, Get_User_Schema

from flask_jwt_extended import jwt_required, get_jwt_identity
from webapp.auth.models import db, User
from webapp.api.user_account.models import UserAffiliates

from flask import request, jsonify, make_response

user_fields = {
    "id": fs.Integer(),
    "login": fs.String(),
    "password": fs.String(),
    "name": fs.String(),
    "lastname": fs.String(),
    "user_type": fs.String(),
    "role_id": fs.Integer(),
    "verified": fs.Boolean(),
}

# Instance of the user repository
user_repository = UserRepository(db, Create_User_Schema, Update_User_Schema)


class UserApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_repository,  # Repositorio de usuarios
            Get_User_Schema,  # Esquema Get para roles
        )
    @jwt_required(fresh=True)
    def put(self):
        user_identity = get_jwt_identity()
        if user_identity:
            response = {"status" : 200, "role" : User.get_role(user_identity)}
            return response, 200
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return response, 401
        
    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            data = request.get_json()

            if data:
                affiliate = UserAffiliates(
                    user_id=user_id,
                    document_number=data.get("identification_document"),
                    name=data.get("name"),
                    phone=data.get("phone"),
                    mail=data.get("email"),
                    wallet=data.get("wallet"),
                )

                db.session.add(affiliate)
                db.session.commit()

                responseObject = {
                    "status": "success",
                    "message": "Successfully added."
                }
                return responseObject, 200
            else:
                responseObject = {
                    "status": "failed",
                    "message": "Something failed."
                }
                return responseObject, 500
            
    @jwt_required(fresh=True)
    def get(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)

            if user_id:
                affiliates = UserAffiliates.query.filter_by(user_id=user_id).all()
                affiliates = [{
                        "id": affiliate.id,
                        "identification_document": affiliate.document_number,
                        "destination": affiliate.name,
                        "phone": affiliate.phone,
                        "email": affiliate.mail,
                        "destination_wallet": affiliate.wallet
                    } for affiliate in affiliates]

                responseObject = {
                    "status": "success",
                    "message": "Successfully retrieved.",
                    "data": affiliates
                }
                return responseObject, 200
            else:
                responseObject = {
                    "status": "failed",
                    "message": "Something failed."
                }
                return responseObject, 500

    @jwt_required(fresh=True)
    def delete(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            data = request.get_json()
            affiliate_id = data.get("affiliate_id")
            affiliate = UserAffiliates.query.filter_by(user_id=user_id, id=affiliate_id).first()
            if affiliate:
                db.session.delete(affiliate)
                db.session.commit()
                responseObject = {
                    "status": "success",
                    "message": "Successfully deleted."
                }
                return responseObject, 200
            else:
                responseObject = {
                    "status": "failed",
                    "message": "Affiliate not found."
                }
                return responseObject, 404


