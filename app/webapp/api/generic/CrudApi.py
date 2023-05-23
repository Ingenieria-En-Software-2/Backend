from flask import abort
from flask_restful import Resource, marshal


class CrudApi(Resource):

    def __init__(self, repository, fields, post_parser, put_parser, get_parser):
        self.repository = repository
        self.fields = fields
        self.post_parser = post_parser
        self.put_parser = put_parser
        self.get_parser = get_parser
        super().__init__()

    def get(self, id=None):        

        if id:
            # Buscar el recurso especifico en la base.
            user = self.repository.get_by_id(id)
            if not user:
                abort(404, 'Resource not found')
            return marshal(user, self.fields)
            
        args = self.get_parser.parse_args()
        if args['page_number'] <= 0 or args['page_size'] <= 0:
            abort(400, "page_number and page_size must be a non zero positive integer")
        print(args)
        results = self.repository.get_all(args['page_number'], args['page_size'], args['sort_by'], args['sort_order'])
        return marshal(results, self.fields)

    def post(self):        

        args = self.post_parser.parse_args(strict=True)
        result = self.repository.create(**args)
        

        if not result:
            abort(500, "Something went wrong creating resource")
        
        return {'id' : result.id}, 201

    def put(self, id=None):        

        if not id:
            abort(400, 'id is required')

        args = self.put_parser.parse_args(strict=True)
        
        try:
            result = self.repository.update(id, **args)
        except ValueError:
            abort(404, 'Resource not found')
        
        if not result:
            abort(500, "Something went wrong updating resource")

        return {'id' : result.id}, 201


    def delete(self, id=None):
        if not id:
            abort(400, 'id is required')

        try:
            result = self.repository.delete(id)
        except ValueError: 
            abort(404, 'Resource not found')

        if result==-1:
            abort(500, "Something went wrong deleting resource")        
        
        return "", 204