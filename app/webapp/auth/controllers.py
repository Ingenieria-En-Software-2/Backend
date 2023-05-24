from flask import Blueprint


auth_blueprint = Blueprint(
'auth',
__name__,
url_prefix="/auth"
)

@auth_blueprint.route('/')
def login():
    return 'I am a Login'