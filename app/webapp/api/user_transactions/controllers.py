"""
Module containing the definition of the UserTransactionsApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort, request
from flask_restful import fields
from webapp.auth.models import db, User
from .models import UserTransaction
from .UserTransactionsRepository import UserTransactionsRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import Get_User_Transaction_Schema

# Instance of the account holder repository
user_transactions_repository = UserTransactionsRepository(db)
import datetime

from marshmallow import (
    ValidationError
)


from webapp.api.user_account.UserAccountRepository import UserAccountRepository


from ..user_account.schemas import (
    Create_User_Account_Schema, Update_User_Account_Schema,
    Get_User_Account_Schema
)


from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

# Instance of the account holder repository
user_account_repository = UserAccountRepository(
    db, Create_User_Account_Schema, Update_User_Account_Schema
)


class UserTransactionsApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_transactions_repository,  # Repositorio de transacciones
            Get_User_Transaction_Schema,  # Esquema Get para roles
        )

    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            data = request.get_json()


            wallet_origin = data.get('origin')
            wallet_destination = data.get('destination')
            amount = data.get('amount')
            trans_type = data.get('transaction_type')
            currency = data.get('currency')
            description = data.get('description')
            status = 2
            
            #verificar si el origen y destino son del mismo dueno, de terceros o de un wallet diferente
            origin = user_account_repository.get_user_account_by_account_number(wallet_origin)
            if not origin:
                return {'code':404, 'error':f'No existe la cuenta de origen: {wallet_origin}'}, 404
            destination = user_account_repository.get_user_account_by_account_number(wallet_destination)
            if not destination:
                return {'code':404, 'error':f'No existe la cuenta de destino: {wallet_destination}:'}
            

            # new_amount = amount
            # if user_origin.user_id != user_destination.user_id and trans_type == "Caribbean Wallet": #2%
            #     new_amount = amount + ((amount*2)/100)
            # elif user_origin.user_id != user_destination.user_id and trans_type != "Caribbean Wallet": #5%
            #     new_amount = amount + ((amount*5)/100)

            
            A = user_transactions_repository.create(**{
                'transaction_type' : trans_type,
                'transaction_date' : str(datetime.datetime.now()),
                'user_id' : user_id,
                'amount' : amount,
                'currency_id' : currency,
                'origin_account': origin.id,
                'destination_account' : destination.id,
                'transaction_status_id' : status,
                'transaction_description' : description
            })
            response = {
                'status' : 200,
                'message' : 'Se ha realizado la transferencia.',
                'transaction_id' : A.id,
            }
            return response, 200

        else:
            response = { "status" : 401, "message": "No se ha iniciado sesión." }
            return response, 401

    @jwt_required(fresh=True)
    def put(self,id):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            A = user_transactions_repository.update(id, **{'transaction_status_id': 3})
            print(A)
            response = {
                'status' : 200,
                'message' : 'Se ha cancelado la transferencia.',
                'id' : A.id
            }
            return response, 200
        else:
            response = { "status" : 401, "message": "No se ha iniciado sesión." }
            return response, 401

    @jwt_required(fresh=True)
    def get(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            A = user_transactions_repository.get_transactions_by_user_id(user_id)
            if len(A) == 0:
                response = { "status" : 400, "message": "No se ha realizado ninguna transferencia." }
                return response, 400
            else:
                B = list(map(lambda x: {"origin" : x.origin_account, "destination" : x.destination_account, "amount" : x.amount,
                                        "transaction_type" : x.transaction_type, "transaction_date" : x.transaction_date.strftime("%m/%d/%Y, %H:%M:%S"), 
                                        "currency" : user_transactions_repository.get_currency_by_currency_id(x.currency_id).name,
                                        "description" : x.transaction_description, "id" : x.id,
                                        "status" : x.transaction_status_id}, A))
                response = { "status" : 200, "transactions": B }
                return response, 200
        else:
            response = { "status" : 401, "message": "No se ha iniciado sesión." }
            return response, 401