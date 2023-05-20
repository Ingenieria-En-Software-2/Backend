from flask import abort, current_app, jsonify, request
from flask_restful import Resource, fields, marshal_with
from .parsers import (
    user_post_parser
)

user_fields = {
    'id' : fields.Integer(),
    'login' : fields.String(),
    'first_name' : fields.String(),
    'last_name' : fields.String()
}

class UserApi(Resource):

    @marshal_with(user_fields)
    def get(self, user_id=None):
        # TODO: Usar la interfaz que se proveera
        
        ##### Codigo para pruebas #####
        if user_id:
            # Buscar el usuario especifico en la base.
            return TESTINGUSER(user_id, 'Santa', 'ho', 'ho')
        else:
            # Retornar los usuarios
            users = [TESTINGUSER(user_id, 'Santa', 'ho', 'ho'), [TESTINGUSER(user_id, 'Pika', 'Chu', 'am')]]
            return users 
        ################################

    def post(self):
        # TODO: Usar la interfaz que se proveera.

        ##### Codigo para pruebas #####
        # Conseguir los datos
        args = user_post_parser.parse_args()
        # Crear el usuario
        print(args)
        # Retornar id del usuario
        id = 2
        return {'id' : id}, 201
        ########################

    def put(self, user_id=None):
        # TODO: Usar la interfaz que se proveera
        if not user_id:
            abort(400, 'user_id is required')

        ##### Codigo para pruebas #####
        # Si no existe el usuario, abort
        # Si existe, aplicar los cambios
        id = user_id
        # Se retorna el id de quien se le aplicaron los cambios
        return {'id' : id}, 201
        ##############################

    def delete(self, user_id=None):
        # TODO: Usar la interfaz que se proveera
        if not user_id:
            abort(400, 'user_id is required')
       
        return "", 204


        

# TESTING
class TESTINGUSER():
    def __init__(self, id, login, name, lastname) -> None:
        self.id = id 
        self.login = login
        self.first_name = name
        self.last_name = lastname