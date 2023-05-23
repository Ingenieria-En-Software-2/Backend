from flask import abort, request
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
        """
        When id is specified, gets the record from the DataBase.
        Otherwise, execute a query and returns the result.

        :return: The resource or a list of resources.
        """
        # Si hay id especificado, se busca en la base.
        if id:            
            user = self.repository.get_by_id(id)
            if not user:
                abort(404, 'Resource not found')
            return marshal(user, self.fields)

        # Consultar los recursos segun los filtros y paginarlos        
        args = self.get_parser.parse_args()
        if args['page_number'] <= 0 or args['page_size'] <= 0:
            abort(400, "page_number and page_size must be a non zero positive integer")
        
        filter_args = {
            key:args[key] for key in args if key not in 
                ['page_number', 'page_size', 'sort_order', 'sort_by'] 
            }
       
        results = self.repository.get_all(
            args['page_number'], args['page_size'], args['sort_by'], 
            args['sort_order'], **filter_args)
        
        if len(results.items) == 0:
            abort(404, "No resources found")
       

        return {
            'next_page' : results.next_num,
            'prev_page' : results.prev_num,
            'item_count' : len(results.items),
            'total_pages' : results.pages,
            'total_items' : results.total,
            'items' : marshal(results.items, self.fields)
        }


    def post(self):        
        """
        Creates a new resource in the database

        :return: The id of the created resource
        """
        args = self.post_parser.parse_args(strict=True)
        result = self.repository.create(**args)
        

        if not result:
            abort(500, "Something went wrong creating resource")
        
        return {'id' : result.id}, 201

    def put(self, id=None):        
        """
        Edits the resource that is identified with id

        :return: The id of the edited resource
        """
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
        """
        Deletes the resource that is identified with id
        """
        if not id:
            abort(400, 'id is required')

        try:
            result = self.repository.delete(id)
        except ValueError: 
            abort(404, 'Resource not found')

        if result==-1:
            abort(500, "Something went wrong deleting resource")        
        
        return "", 204