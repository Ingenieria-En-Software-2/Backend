from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from flask import jsonify
from webapp.api import rest_api_bp
from webapp.repositories.exceptions import IdNotProvided
import marshmallow
import sqlalchemy
import re


@rest_api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=f"Resource not found", code=404), 404


@rest_api_bp.errorhandler(marshmallow.ValidationError)
def validation_error(e):
    return jsonify(errors=e.messages), 400


@rest_api_bp.errorhandler(IdNotProvided)
def id_not_provided(e):
    return jsonify(error="You must provide an ID in the URL"), 400


@rest_api_bp.errorhandler(sqlalchemy.exc.IntegrityError)
def integrity_error(e):
    if isinstance(e.orig, UniqueViolation):
        violation_key = re.search(r"\(\w+\)", e.orig.pgerror).group(0).strip("()")

        return jsonify(error={f"{violation_key}": "already in use"}), 400

    if isinstance(e.orig, ForeignKeyViolation):
        details = e.orig.pgerror.split("\n")[1]
        violation_key = re.search(r"\(\w+\)", details).group(0).strip("()")
        details = details[9:]
        return jsonify(error={f"{violation_key}": details}), 400

    return jsonify(msg=f"You found an unhandled exception!"), 400
