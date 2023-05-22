from flask import abort, current_app, jsonify, request
from flask_restful import Resource, fields, marshal_with
from webapp.auth.UserRepository import UserRepository
from .parsers import (
    user_post_parser
)

user_fields = {
    'id' : fields.Integer(),
    'login' : fields.String(),
    'first_name' : fields.String(),
    'last_name' : fields.String()
}

#user_repository = UserRepository(User, db)

class UserApi(Resource):

    @marshal_with(user_fields)
    def get(self, user_id=None):
        # TODO: Usar la interfaz que se proveera
        # TODO: Agregar argumentos para busquedas especificas y paginacion
        # TODO: Comprobar caso que no existe el usuario o error de paginacion.
        
        ##### Codigo para pruebas #####
        if user_id:
            # Buscar el usuario especifico en la base.
            # return user_repository.get_by_id(user_id)
            return TESTINGUSER(user_id, 'Santa', 'ho', 'ho')
        else:
            # Retornar los usuarios
            # return user_repository.get_all()
            users = [TESTINGUSER(1, 'Santa', 'ho', 'ho'), [TESTINGUSER(2, 'Pika', 'Chu', 'am')]]
            return users 
        ################################

    def post(self):
        # TODO: Usar la interfaz que se proveera.
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        args = user_post_parser.parse_args()
        # result = user_repository.create(args)



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
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        if not user_id:
            abort(400, 'user_id is required')

        # result = user_repository.update(args)
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

        # user_repository.delete(user_id)
        
        return "", 204


        

# TESTING
class TESTINGUSER():
    def __init__(self, id, login, name, lastname) -> None:
        self.id = id 
        self.login = login
        self.first_name = name
        self.last_name = lastname