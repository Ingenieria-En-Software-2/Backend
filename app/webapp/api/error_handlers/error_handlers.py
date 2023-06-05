
from flask import jsonify
from webapp.api import rest_api_bp

@rest_api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=f'Resource not found', code=404), 404