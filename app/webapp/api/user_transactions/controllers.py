"""
Module containing the definition of the UserTransactionsApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from flask import abort, request
from flask_restful import fields
from webapp.auth.models import db, User, Role, Wallet
from .models import UserTransaction
from .UserTransactionsRepository import UserTransactionsRepository
from webapp.api.generic.CrudApi import CrudApi
from .schemas import Get_User_Transaction_Schema
from webapp.api.logger.models import LogEvent

# Instance of the account holder repository
user_transactions_repository = UserTransactionsRepository(db)
from datetime import datetime

from marshmallow import ValidationError


from webapp.api.user_account.UserAccountRepository import UserAccountRepository
from webapp.api.account_holder.AccountHolderRepository import AccountHolderRepository


from ..user_account.schemas import (
    Create_User_Account_Schema,
    Update_User_Account_Schema,
    Get_User_Account_Schema,
)

from ..account_holder.schemas import (
    Create_Account_Holder_Schema,
    Update_Account_Holder_Schema,
    Get_Account_Holder_Schema,
)


from flask_jwt_extended import jwt_required, get_jwt_identity

from webapp.auth.email_verification import send_transaction_email, send_pago_movil_email


# Instance of the user account repository
user_account_repository = UserAccountRepository(
    db, Create_User_Account_Schema, Update_User_Account_Schema
)

# Instance of the account holder repository
account_holder_repository = AccountHolderRepository(
    db, Create_Account_Holder_Schema, Update_Account_Holder_Schema
)


class UserTransactionsApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            user_transactions_repository,  # Repositorio de transacciones
            Get_User_Transaction_Schema,  # Esquema Get para roles
        )

    def handle_inter_wallet_transaction(
        self, user_id, origin, destination, amount, currency, description, status
    ):
        origin = user_account_repository.get_user_account_by_account_number(origin)
        if not origin or origin == None:
            return {
                "status": 404,
                "message": f"No existe la cuenta de origen: {origin}",
            }, 404
        try:
            A = user_transactions_repository.create(
                **{
                    "transaction_type": "inter_wallet",
                    "transaction_date": str(datetime.now()),
                    "user_id": user_id,
                    "amount": amount,
                    "currency_id": user_transactions_repository.get_currency_by_currency_name(
                        currency
                    ).id,
                    "origin_account": origin.id,
                    "destination_account": 1,
                    "transaction_status_id": status,
                    "transaction_description": description,
                }
            )
            user_login = db.session.query(User).filter(User.id == user_id).first()
            send_transaction_email(
                "inter_wallet",
                user_login.login,
                origin.account_number,
                destination,
                amount,
                currency,
            )
            if status == 2:
                response = {
                    "status": 200,
                    "message": "Se ha realizado la transferencia Interwallet.",
                    "transaction_id": A.id,
                }
                log = LogEvent(user_id=user_id, description="Transferencia realizada")
                db.session.add(log)
                db.session.commit()
                return response, 200
            elif status == 1:
                response = {
                    "status": 201,
                    "message": "Su transferencia ha sido retenida",
                    "transaction_id": A.id,
                }
                log = LogEvent(user_id=user_id, description="Transferencia retenida")
                db.session.add(log)
                db.session.commit()
                return response, 201
        except Exception as e:
            response = {
                "status": 500,
                "message": "La moneda no existe.",
            }

            return response, 500

    def handle_pago_movil(
        self,
        origin,
        dest_CI,
        dest_name,
        dest_phone,
        dest_wallet,
        description,
        amount,
        currency,
        user_id,
        status,
    ):
        origin = user_account_repository.get_user_account_by_account_number(origin)
        if not origin or origin == None:
            return {
                "status": 404,
                "message": f"No existe la cuenta de origen: {origin}",
            }, 404
        try:
            wallet = (
                db.session.query(Wallet).filter(Wallet.id == int(dest_wallet)).first()
            )
            print(f"wallet : {wallet.description}")
            if not wallet or wallet == None:
                response = {
                    "status": 404,
                    "message": f"No existe la wallet: {wallet}",
                }
                return make_response(jsonify(response)), 404
            if wallet.description != "Caribbean Wallet":
                destination_acc = 1
            else:
                acc = account_holder_repository.get_account_holder_by_phone(dest_phone)
                if not acc or acc == None:
                    response = {
                        "status": 404,
                        "message": f"El telefono: {dest_phone} no esta asociado a ningun usuario",
                    }
                    return make_response(jsonify(response)), 404
                destination_acc = user_account_repository.get_user_account_by_id(
                    acc.user_id
                ).id

            A = user_transactions_repository.create(
                **{
                    "transaction_type": "pago_movil",
                    "transaction_date": str(datetime.now()),
                    "user_id": user_id,
                    "amount": amount,
                    "currency_id": user_transactions_repository.get_currency_by_currency_name(
                        currency
                    ).id,
                    "origin_account": origin.id,
                    "destination_account": destination_acc,
                    "transaction_status_id": status,
                    "transaction_description": description,
                }
            )
            user_login = db.session.query(User).filter(User.id == user_id).first()
            send_pago_movil_email(
                user_login.login,
                origin.account_number,
                dest_CI,
                dest_name,
                wallet.description,
                amount,
                currency,
            )
            if status == 2:
                response = {
                    "status": 200,
                    "message": "Se ha realizado la transferencia Pago Movil.",
                    "transaction_id": A.id,
                }
                return response, 200
            elif status == 1:
                response = {
                    "status": 201,
                    "message": "Su transferencia ha sido retenida",
                    "transaction_id": A.id,
                }
                return response, 201
        except Exception as e:
            response = {
                "status": 500,
                "message": "La moneda no existe.",
            }
            return response, 500

    def check_status(self, amount):
        stat = 2
        if float(amount) > 1000:
            stat = 1
        return stat

    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            data = request.get_json()

            trans_type = data.get("transaction_type")
            status = self.check_status(data.get("amount"))

            if trans_type == "pago_movil":
                wallet_origin = data.get("origin")
                dest_CI = data.get("destination_ci")
                dest_wallet = data.get("destination_wallet")
                dest_name = data.get("destination_name")
                dest_phone = data.get("destination_phone")
                description = data.get("description")
                currency = data.get("currency")
                amount = data.get("amount")
                return self.handle_pago_movil(
                    wallet_origin,
                    dest_CI,
                    dest_name,
                    dest_phone,
                    dest_wallet,
                    description,
                    amount,
                    currency,
                    user_id,
                    status,
                )

            wallet_origin = data.get("origin")
            wallet_destination = data.get("destination")
            amount = data.get("amount")
            currency = data.get("currency")
            description = data.get("description")
            if trans_type == "inter_wallet":
                return self.handle_inter_wallet_transaction(
                    user_id,
                    wallet_origin,
                    wallet_destination,
                    amount,
                    currency,
                    description,
                    status,
                )

            # verificar si el origen y destino existen
            origin = user_account_repository.get_user_account_by_account_number(
                wallet_origin
            )
            if not origin or origin == None:
                return {
                    "status": 404,
                    "message": f"No existe la cuenta de origen: {wallet_origin}",
                }, 404
            destination = user_account_repository.get_user_account_by_account_number(
                wallet_destination
            )
            if (
                not destination or destination == None
            ) and trans_type != "inter_wallet":
                return {
                    "status": 404,
                    "message": f"No existe la cuenta de destino: {wallet_destination}",
                }, 404

            if origin.user_id == destination.user_id and trans_type != "b_a":
                return {
                    "status": 414,
                    "message": 'Para realizar transferencias del mismo usuario, ir a la seccion "Entre Cuentas".',
                }, 414

            try:
                A = user_transactions_repository.create(
                    **{
                        "transaction_type": trans_type,
                        "transaction_date": str(datetime.now()),
                        "user_id": user_id,
                        "amount": amount,
                        "currency_id": user_transactions_repository.get_currency_by_currency_name(
                            currency
                        ).id,
                        "origin_account": origin.id,
                        "destination_account": destination.id,
                        "transaction_status_id": status,
                        "transaction_description": description,
                    }
                )
                user_login = db.session.query(User).filter(User.id == user_id).first()
                send_transaction_email(
                    "transaction",
                    user_login.login,
                    origin.account_number,
                    destination.account_number,
                    amount,
                    currency,
                )
                if status == 2:
                    response = {
                        "status": 200,
                        "message": "Se ha realizado la transferencia.",
                        "transaction_id": A.id,
                    }
                    log = LogEvent(
                        user_id=user_id, description="Transferencia realizada"
                    )
                    db.session.add(log)
                    db.session.commit()
                    return response, 200
                elif status == 1:
                    response = {
                        "status": 201,
                        "message": "Su transferencia ha sido retenida",
                        "transaction_id": A.id,
                    }
                    log = LogEvent(
                        user_id=user_id, description="Transferencia retenida"
                    )
                    db.session.add(log)
                    db.session.commit()
                    return response, 201
            except Exception as e:
                print(e)
                response = {
                    "status": 500,
                    "message": "La moneda no existe.",
                }
                return response, 500
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return response, 401

    @jwt_required(fresh=True)
    def put(self, id, status):
        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            if (
                User.get_role(user_identity) == 1
            ):  # es administrador y puede cancelar la transferencia    #user_id == A.user_id:
                try:
                    A = user_transactions_repository.update(
                        id, **{"transaction_status_id": status}
                    )
                    mess = ""
                    des = ""
                    if status == 1:
                        mess = "Se ha cancelado la transferencia."
                        des = "Transferencia Cancelada"
                    if status == 2:
                        mess = "Se ha aprobado la transferencia."
                        des = "Transferencia Aprobada"
                    response = {
                        "status": 200,
                        "message": mess,
                        "id": A.id,
                    }
                    log = LogEvent(user_id=user_id, description=des)
                    db.session.add(log)
                    db.session.commit()
                    return response, 200
                except ValidationError as inst:
                    response = {
                        "status": 500,
                        "message": list(inst.messages.values())[0][0],
                    }
                    return response, 500
            else:
                response = {
                    "status": 400,
                    "message": "La transferencia solo puede ser cancelada por un usuario administrador.",
                }
                return response, 400
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return response, 401

    def get_transactions_by(self, g, inp, user_id, role, account_type):
        if g == "today":
            A = user_transactions_repository.get_transactions_by_day(
                datetime.now().strftime("%Y-%m-%d"), role, user_id, account_type
            )
        elif g == "week":
            A = user_transactions_repository.get_transactions_by_week(
                role, user_id, account_type
            )
        elif g == "month":
            A = user_transactions_repository.get_transactions_by_month(
                int(inp), role, user_id, account_type
            )
        elif g == "quarter":
            A = user_transactions_repository.get_transactions_by_quarter(
                int(inp), role, user_id, account_type
            )
        elif g == "year":
            A = user_transactions_repository.get_transactions_by_year(
                int(inp), role, user_id, account_type
            )
        elif g == "date":
            date = (datetime.strptime(inp, "%Y-%m-%d")).strftime("%Y-%m-%d")
            A = user_transactions_repository.get_transactions_by_date(
                date, role, user_id, account_type
            )
        elif g == "period":
            start = (datetime.strptime(inp.split(" ")[0], "%Y-%m-%d")).strftime(
                "%Y-%m-%d"
            )
            end = (datetime.strptime(inp.split(" ")[1], "%Y-%m-%d")).strftime(
                "%Y-%m-%d"
            )
            A = user_transactions_repository.get_transactions_by_period(
                start, end, role, user_id, account_type
            )
        if g == "all":
            A = user_transactions_repository.get_all_transactions(
                role, user_id, account_type
            )
        return A

    def type_of_transaction(self, t):
        if t == "inter_wallet":
            return "Inter Wallet"
        elif t == "b_a":
            return "Entre cuentas"
        elif t == "to_3rds":
            return "A Terceros"
        elif t == "pago_movil":
            return "Pago Móvil"

    def get_ci(self, x):
        AH = account_holder_repository.get_account_holder_by_user_id(
            user_account_repository.get_user_account_by_id(x).user_id
        )
        if AH == None:
            return -1
        else:
            return AH.id_number

    @jwt_required(fresh=True)
    def get(self, g, inp, account_type):
        """
        This function returns the transactions
        :param g: Filter we wanna apply for the search, it can be "all","today","week","month","quarter","year","date","period"
        :param inp: Specified search for "month","quarter","year","date","period"
        :param inp: Account type of the transactions done by said account, 1 is for checking, 2 is for savings, 0 for admins
        that gather any
        :return: All the transactions filtered by g and inp

        inp can be any string for "all","today","week"

        inp has to be:
        month -> the number of the month
        quarter -> the number of the quarter of the year
        date -> the date in format %Y-%m-%d
        period -> A string that contains both dates in format %Y-%m-%d and separated by a space

        The transactions are given depending on the role of the user
        If the user is admin, the transactions returned are all of the ones that comply with the filter
        If the user has role user, the transactions are filtered also only by theirs id
        """

        # 1 es corriente
        # 2 es ahorro

        user_identity = get_jwt_identity()
        if user_identity:
            user_id = User.decode_token(user_identity)
            try:
                A = self.get_transactions_by(
                    g, inp, user_id, User.get_role(user_identity), account_type
                )
                if len(A) == 0:
                    response = {
                        "status": 400,
                        "message": "No se ha realizado ninguna transferencia.",
                    }
                    return response, 400
                else:
                    B = list(
                        map(
                            lambda x: {
                                "origin": x.origin_account,
                                "user_name_origin": db.session.query(User)
                                .filter(
                                    User.id
                                    == user_account_repository.get_user_account_by_id(
                                        x.origin_account
                                    ).user_id
                                )
                                .first()
                                .name,
                                "destination": x.destination_account,
                                "amount": x.amount,
                                "transaction_id": x.id,
                                "ci": self.get_ci(x.origin_account),
                                "description": x.transaction_description,
                                "transaction_type": self.type_of_transaction(
                                    x.transaction_type
                                ),
                                "transaction_date": x.transaction_date.strftime(
                                    "%m/%d/%Y"
                                ),
                                "transaction_hour": x.transaction_date.strftime(
                                    "%H:%M:%S"
                                ),
                                "currency": user_transactions_repository.get_currency_by_currency_id(
                                    x.currency_id
                                ).name,
                                "status": x.transaction_status_id,
                            },
                            A,
                        )
                    )
                    response = {"status": 200, "transactions": B}
                    return response, 200
            except Exception as e:
                response = {"status": 500, "message": "Un error ha ocurrido"}
                return response, 500
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return response, 401
