from flask import abort
from flask_restful import Resource, fields, marshal_with
from webapp.auth.models import db, User
from webapp.auth.UserRepository import UserRepository
from .parsers import (
    user_post_parser,
    user_put_parser
)

user_fields = {
    'id' : fields.Integer(),
    'login' : fields.String(),
    'password' : fields.String(),
    'name' : fields.String(),
    'lastname' : fields.String(),
    'user_type' : fields.String(),
    'role_id' : fields.Integer(),
}

user_repository = UserRepository(db)

class UserApi(Resource):

    @marshal_with(user_fields)
    def get(self, user_id=None):        
        # TODO: Agregar argumentos para busquedas especificas y paginacion
        # TODO: Comprobar caso que no existe el usuario o error de paginacion.
        if user_id:
            # Buscar el usuario especifico en la base.
            user = user_repository.get_by_id(user_id)
            if not user:
                abort(404, 'User not found')
            return user
            
        else:
            # Retornar los usuarios
            return user_repository.get_all()            

    def post(self):        
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        args = user_post_parser.parse_args()
        result = user_repository.create(**args)
        
        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something whent wrong creating resource")
        
        return result.id, 201

    def put(self, user_id=None):        
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        if not user_id:
            abort(400, 'user_id is required')

        args = user_put_parser.parse_args()
        result = user_repository.update(user_id, **args)

        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something whent wrong updating resource")

        return {'id' : result.id}, 201


    def delete(self, user_id=None):
        if not user_id:
            abort(400, 'user_id is required')

        result = user_repository.delete(user_id)
        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something whent wrong deleting resource")        
        
        return "", 204

