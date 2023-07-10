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

    def handle_inter_wallet_transaction(self, user_id, origin,destination,amount,currency,description):
        origin = user_account_repository.get_user_account_by_account_number(origin)
        if not origin or origin==None:
            return {'status':404, 'message':f'No existe la cuenta de origen: {wallet_origin}'}, 404
        try:
            A = user_transactions_repository.create(**{
                'transaction_type' : 'inter_wallet',
                'transaction_date' : str(datetime.datetime.now()),
                'user_id' : user_id,
                'amount' : amount,
                'currency_id' : user_transactions_repository.get_currency_by_currency_name(currency).id,
                'origin_account': origin.id,
                'destination_account' : 1,
                'transaction_status_id' : 2,
                'transaction_description' : description
            })
            response = {
                'status' : 200,
                'message' : 'Se ha realizado la transferencia Interwallet.',
                'transaction_id' : A.id,
            }
            return response, 200
        except Exception as e:
            response = {
                'status' : 500,
                'message' : 'La moneda no existe.',
            }
            return response, 500


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

            if trans_type == "inter_wallet":
                return self.handle_inter_wallet_transaction(user_id, wallet_origin, wallet_destination,amount, currency, description)

            #verificar si el origen y destino existen
            origin = user_account_repository.get_user_account_by_account_number(wallet_origin)
            if not origin or origin==None:
                return {'status':404, 'message':f'No existe la cuenta de origen: {wallet_origin}'}, 404
            destination = user_account_repository.get_user_account_by_account_number(wallet_destination)
            if (not destination or destination==None) and trans_type != "inter_wallet":
                return {'status':404, 'message':f'No existe la cuenta de destino: {wallet_destination}'}, 404

            if origin.user_id == destination.user_id and trans_type != 'b_a':
                return {'status' : 414, 'message' : 'Para realizar transferencias del mismo usuario, ir a la seccion "Entre Cuentas".'}, 414
            
            try:
                A = user_transactions_repository.create(**{
                    'transaction_type' : trans_type,
                    'transaction_date' : str(datetime.datetime.now()),
                    'user_id' : user_id,
                    'amount' : amount,
                    'currency_id' : user_transactions_repository.get_currency_by_currency_name(currency).id,
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
            except Exception as e:
                response = {
                    'status' : 500,
                    'message' : 'La moneda no existe.',
                }
                return response, 500
        else:
            response = { "status" : 401, "message": "No se ha iniciado sesión." }
            return response, 401

    @jwt_required(fresh=True)
    def put(self,id):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            A = user_transactions_repository.update(id, **{'transaction_status_id': 3})
            if user_id == A.user_id: 
                try:
                    B = user_transactions_repository.create(**{
                        'transaction_type' : A.transaction_type,
                        'transaction_date' : str(datetime.datetime.now()),
                        'user_id' : user_id,
                        'amount' : A.amount,
                        'currency_id' : A.currency_id,
                        'origin_account': A.destination_account,
                        'destination_account' : A.origin_account,
                        'transaction_status_id' : A.transaction_status_id,
                        'transaction_description' : A.transaction_description
                    })
                    response = {
                        'status' : 200,
                        'message' : 'Se ha cancelado la transferencia.',
                        'id' : B.id
                    }
                    return response, 200
                except ValidationError as inst:
                    response = {
                        'status' : 500,
                        'message' : list(inst.messages.values())[0][0]
                    }
                    return response, 500
            else:
                response = {
                        'status' : 400,
                        'message' : "La transferencia solo puede ser cancelada por el usuario que la realizó."
                    }
                return response, 400
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
                                        "status" : x.transaction_status_id}, A))
                response = { "status" : 200, "transactions": B }
                return response, 200
        else:
            response = { "status" : 401, "message": "No se ha iniciado sesión." }
            return response, 401
