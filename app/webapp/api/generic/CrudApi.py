from flask import abort
from flask_restful import Resource, marshal


class CrudApi(Resource):

    def __init__(self, repository, fields, post_parser, put_parser):
        self.repository = repository
        self.fields = fields
        self.post_parser = post_parser
        self.put_parser = put_parser
        super().__init__()

    def get(self, id=None):        
        # TODO: Agregar argumentos para busquedas especificas y paginacion
        # TODO: Comprobar caso que no existe el recurso o error de paginacion.
        if id:
            # Buscar el usuario especifico en la base.
            user = self.repository.get_by_id(id)
            if not user:
                abort(404, 'Resource not found')
            return marshal(user, self.fields)
            
        else:
            # Retornar los usuarios
            return marshal(self.repository.get_all(), self.fields)

    def post(self):        
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        args = self.post_parser.parse_args(strict=True)
        result = self.repository.create(**args)
        
        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something went wrong creating resource")
        
        return result.id, 201

    def put(self, id=None):        
        # TODO: Comprobar caso con campos extras
        # TODO: Comprobar caso con error
        if not id:
            abort(400, 'id is required')

        args = self.put_parser.parse_args(strict=True)
        print(args)
        result = self.repository.update(id, **args)

        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something went wrong updating resource")

        return {'id' : result.id}, 201


    def delete(self, id=None):
        if not id:
            abort(400, 'id is required')

        result = self.repository.delete(id)
        # TODO: Mejorar este codigo de error
        if not result:
            abort(500, "Something went wrong deleting resource")        
        
        return "", 204