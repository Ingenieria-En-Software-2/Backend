
from flask import jsonify
from webapp.api import rest_api_bp
import marshmallow

@rest_api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=f'Resource not found', code=404), 404

@rest_api_bp.errorhandler(marshmallow.ValidationError)
def validation_error(e):
    print(e.messages)
    return jsonify(errors=e.messages, code=400), 400