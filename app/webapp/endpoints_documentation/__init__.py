"""

Module for documentation of the api and backend endpoints. Built with Swagger on 
the specified path, using de flask-swagger-ui module

Access path to the documentation
- /api/doc

"""

def create_documentation(app, **kwargs):
    from flask_swagger_ui import get_swaggerui_blueprint 
    SWAGGER_URL = '/docs' # URL for exposing Swagger UI
    API_URL = '/static/docs/v1/swagger.yaml'    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        }
    )
    app.register_blueprint(swaggerui_blueprint)
    