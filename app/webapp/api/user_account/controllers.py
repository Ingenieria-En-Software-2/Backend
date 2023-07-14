"""
Module containing the definition of the UserAccountApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort, make_response, jsonify, request
from flask_restful import fields
from ...auth.models import db, User
from ...api.user_account.UserAccountRepository import UserAccountRepository
from ...api.user_transactions.UserTransactionsRepository import (
    UserTransactionsRepository,
)
from ...api.generic.CrudApi import CrudApi
import json

from .schemas import (
    Create_User_Account_Schema,
    Update_User_Account_Schema,
    Get_User_Account_Schema,
)
from marshmallow import ValidationError

# Instance of the account holder repository
transaction_repository = UserTransactionsRepository(db)
user_account_repository = UserAccountRepository(db, transaction_repository)

from flask_jwt_extended import jwt_required, get_jwt_identity


class UserAccountApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_account_repository,  # Repositorio de usuarios
            Get_User_Account_Schema,  # Esquema Get
        )

    @jwt_required(fresh=True)
    def get(self):
        # id es el user_id
        # account_type_id 1 es corriente, 2 es ahorro
        user_identity = get_jwt_identity()
        if user_identity:
            resp = User.decode_token(user_identity)
            user_accounts = user_account_repository.get_user_accounts_by_user_id(resp)
            corriente = list(filter(lambda x: x.account_type_id == 1, user_accounts))
            ahorro = list(filter(lambda x: x.account_type_id == 2, user_accounts))
            response = {
                "status": 200,
                "corriente": list(map(lambda x: x.account_number, corriente)),
                "ahorro": list(map(lambda x: x.account_number, ahorro)),
            }
            return response, 200
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return make_response(jsonify(response)), 401

    @jwt_required(fresh=True)
    def put(self):
        #return the amount of money of the account_num passed as a parameter
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            account_number = request.args["account"]
            account_id = user_account_repository.get_user_account_by_account_number(account_number).id
            balance = user_account_repository.get_account_balance(account_id)
            response = {
                "status": 200,
                "balance" : balance["balance"],
            }
            return response, 200
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return make_response(jsonify(response)), 401



    # def post(self):
    #     result = self.repository.create(**request.get_json())

    #     if not result:
    #         abort(500, "Algo salio mal creando el recurso")

    #     return {"id": result.id, "account_number": result.account_number}, 201

    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()

        if user_identity:
            resp = User.decode_token(user_identity)
            request.json["user_id"] = resp
            result = self.repository.create(**request.get_json())
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return make_response(jsonify(response)), 401

        if not result:
            abort(500, "Algo salio mal creando el recurso")

        return {"id": result.id, "account_number": result.account_number}, 201
