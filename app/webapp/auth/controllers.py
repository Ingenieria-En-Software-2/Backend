from sqlalchemy import func
from flask import render_template, Blueprint, flash, redirect, url_for


auth_blueprint = Blueprint(
'auth',
__name__,
url_prefix="/auth"
)

@auth_blueprint.route('/')
def login():
    return 'I am a Login'