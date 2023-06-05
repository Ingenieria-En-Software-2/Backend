
from flask import jsonify
from webapp.api import rest_api_bp

@rest_api_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=f'Resource aaaaaaaaa not found {e}', code=404), 404