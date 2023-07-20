"""
Module containing the definition of the MobilePaymentConfig class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""

from ...api.mobile_payment_config.MobilePaymentConfigRepository import MobilePaymentConfigRepository as MP
from flask import abort, make_response, jsonify, request
from flask_restful import fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...auth.models import db, User
from webapp.api.logger.models import LogEvent
from ...api.generic.CrudApi import CrudApi
from .schemas import (
    POST_Mobile_Payment_Schema,
    GET_Mobile_Payment_Schema
)

# Instance of the Mobile Payment Config repository
mobile_payment_config_repository = MP(
    db, POST_Mobile_Payment_Schema, POST_Mobile_Payment_Schema
)


class MobilePaymentConfigAPI(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            mobile_payment_config_repository,  # Repositoy of Mobile Payment Config
            GET_Mobile_Payment_Schema,  # GET Schema for Mobile Payment Config
        )
        
    @jwt_required(fresh=True)
    def get(self):
        # id es el user_id
        # account_type_id 1 es corriente, 2 es ahorro
        user_identity = get_jwt_identity()
        if user_identity:
            resp = User.decode_token(user_identity)
            configuration = mobile_payment_config_repository.get_config_by_user_id(resp)
            response = {
                "status": 200,
                "response": configuration,
            }
            return response, 200
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return make_response(jsonify(response)), 401
        
    @jwt_required(fresh=True)
    def post(self):
        user_identity = get_jwt_identity()

        if user_identity:
            resp = User.decode_token(user_identity)
            configuration = mobile_payment_config_repository.get_config_by_user_id(resp)
            
            # If configuration exists, update it
            if configuration:
                for key, value in configuration.items():
                    # Check if the key exists in the model and update it
                    if hasattr(self.model, key):
                        setattr(configuration, key, value)
                log = LogEvent(user_id=resp, description="Configuracion de Pago Movil actualizado")
                db.session.commit()
            
            # If configuration does not exist, create it
            else:
                request.json["user_id"] = resp
                result = self.repository.create(**request.get_json())
                log = LogEvent(user_id=resp, description="Configuracion de Pago Movil creado")
                db.session.add(log)
                db.session.commit()
                
        
        else:
            response = {"status": 401, "message": "No se ha iniciado sesión."}
            return make_response(jsonify(response)), 401

        if not result:
            abort(500, "Algo salio mal creando el recurso")

        return {"status": "Solicitud Procesada Correctamente"}, 201
