from flask import abort, request
from flask_restful import Resource


class CrudApi(Resource):
    def __init__(self, repository, get_schema):
        self.repository = repository
        self.get_schema = get_schema
        super().__init__()

    def get(self, id=None):
        """
        When id is specified, gets the record from the DataBase.
        Otherwise, execute a query and returns the result.

        :return: The resource or a list of resources.
        """

        # Si hay id especificado, se busca en la base.
        if id:
            resource = self.repository.get_by_id(id)
            if not resource:
                abort(404)

            return self.repository.schema_create().dump(resource)

        # Consultar los recursos segun los filtros y paginarlos
        args = self.get_schema().load(request.args)

        filter_args = {
            key: args[key]
            for key in args
            if key not in ["page_number", "page_size", "sort_order", "sort_by"]
        }

        results = self.repository.get_all(
            args["page_number"],
            args["page_size"],
            args["sort_by"],
            args["sort_order"],
            **filter_args
        )

        if len(results.items) == 0:
            abort(404)

        return {
            "next_page": results.next_num,
            "prev_page": results.prev_num,
            "item_count": len(results.items),
            "total_pages": results.pages,
            "total_items": results.total,
            "items": self.repository.schema_create(many=True).dump(results.items),
        }

    def post(self):
        """
        Creates a new resource in the database

        :return: The id of the created resource
        """
        print(request.get_json())
        result = self.repository.create(**request.get_json())

        return {"id": result.id}, 201

    def put(self, id=None):
        """
        Edits the resource that is identified with id

        :return: The id of the edited resource
        """
        print(request.get_json())
        result = self.repository.update(id, **request.get_json())

        return {"id": result.id}, 201

    def delete(self, id=None):
        """
        Deletes the resource that is identified with id
        """
        self.repository.delete(id)

        return "", 204
