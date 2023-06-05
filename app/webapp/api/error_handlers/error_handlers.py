from psycopg2.errors import UniqueViolation
from flask import jsonify
from webapp.api import rest_api_bp
import marshmallow
import sqlalchemy
import re


@rest_api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=f'Resource not found', code=404), 404

@rest_api_bp.errorhandler(marshmallow.ValidationError)
def validation_error(e):
    
    return jsonify(errors=e.messages, code=400), 400

@rest_api_bp.errorhandler(sqlalchemy.exc.IntegrityError)
def integrity_error(e):
    if isinstance(e.orig, UniqueViolation):      
        violation_key = re.search(
            r'\(\w+\)', e.orig.pgerror).group(0).strip('()')

        return jsonify(errors={
            f'{violation_key}': 'already in use' 
            }, code=400), 400