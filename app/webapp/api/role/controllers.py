from flask import abort
from flask_restful import Resource, fields, marshal_with
from .parsers import (
    role_post_parser    
)

role_fields = {
    'id' : fields.Integer(),
    'description' : fields.String(),
}


class RoleApi(Resource):

    @marshal_with(role_fields)
    def get(self, role_id=None):
        # TODO: Usar la interfaz que se proveera

        ##### Codigo para pruebas #####
        if role_id:
            # Buscar el role especifico en la base.
            return TESTINGROLE(role_id, 'admin')
        else:
            # Retornar los roles
            roles = [TESTINGROLE(1, 'admin'), [TESTINGROLE(2, 'customer')]]
            return roles 
        ################################

    def post(self):
        # TODO: Usar la interfaz que se proveera.

        ##### Codigo para pruebas #####
        # Conseguir los datos
        args = role_post_parser.parse_args()
        # Crear el role
        print(args)
        # Retornar id del role
        id = 3
        return {'id' : id}, 201
        ########################

    def put(self, role_id=None):
        # TODO: Usar la interfaz que se proveera
        if not role_id:
            abort(400, 'role_id is required')

        ##### Codigo para pruebas #####
        # Si no existe el usuario, abort
        # Si existe, aplicar los cambios

        print('Updated role')
        id = role_id
        # Se retorna el id de quien se le aplicaron los cambios
        return {'id' : id}, 201
        ##############################
          
    def delete(self, role_id=None):
        # TODO: Usar la interfaz que se proveera
        if not role_id:
            abort(400, 'user_id is required')
       
        print('Deleted role')
        return "", 204
        

# TESTING
class TESTINGROLE():
    def __init__(self, id, description) -> None:
        self.id = id 
        self.description = description
