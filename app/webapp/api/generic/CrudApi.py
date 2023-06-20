from flask import abort, request, url_for, render_template
from flask_mail import Mail
from flask_restful import Resource, marshal
from webapp.auth.token import *


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

        result = self.repository.create(**request.get_json())

        if not result:
            abort(500, "Algo salio mal creando el recurso")

        # Crear token de verificacion y enviar correo para verificar usuario
        args = request.get_json()
        if args.get("user_type") == "user":
            mail = Mail()
            token = generate_token(args["login"])
            confirm_url = url_for("auth.verify_api", token=token, _external=True)
            print(confirm_url)
            html = render_template("confirm_email.html", confirm_url=confirm_url)
            email = create_email(args["login"], "Confirm your email", html)

            try:
                mail.send(email)
            except:
                pass

        return {"id": result.id}, 201

    def put(self, id=None):
        """
        Edits the resource that is identified with id

        :return: The id of the edited resource
        """

        result = self.repository.update(id, **request.get_json())

        return {"id": result.id}, 201

    def delete(self, id=None):
        """
        Deletes the resource that is identified with id
        """
        self.repository.delete(id)

        return "", 204
