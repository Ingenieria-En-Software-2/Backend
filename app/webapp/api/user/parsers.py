"""
Módulo que contiene definiciones de parsers para la gestión de usuarios en la
API.

Se definen tres parsers: user_post_parser, user_put_parser y user_get_parser, 
cada uno con sus respectivos argumentos y reglas de validación.
"""

from flask_restful import reqparse
from ..generic.parsers import generic_get_parser


# Parser para la creación de usuarios
user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    "login",
    type=str,
    required=True,
    help="login is required",
    location=("json", "values"),
)

user_post_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="password is required",
    location=("json", "values"),
)

user_post_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="name is required",
    location=("json", "values"),
)

user_post_parser.add_argument(
    "lastname",
    type=str,
    required=True,
    help="lastname is required",
    location=("json", "values"),
)

user_post_parser.add_argument(
    "user_type",
    type=str,
    required=True,
    help="user_type is required",
    location=("json", "values"),
)

user_post_parser.add_argument(
    "role_id",
    type=int,
    required=True,
    help="role_id is required",
    location=("json", "values"),
)

# Parser para la actualización de usuarios
user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument(
    "login",
    type=str,
    location=("json", "values"),
    store_missing=False,
)

user_put_parser.add_argument(
    "password",
    type=str,
    location=("json", "values"),
    store_missing=False,
)

user_put_parser.add_argument(
    "name",
    type=str,
    location=("json", "values"),
    store_missing=False,
)

user_put_parser.add_argument(
    "lastname",
    type=str,
    location=("json", "values"),
    store_missing=False,
)

user_put_parser.add_argument(
    "user_type",
    type=str,
    location=("json", "values"),
    store_missing=False,
)

user_put_parser.add_argument(
    "role_id",
    type=int,
    location=("json", "values"),
    store_missing=False,
)

# Parser para la obtención de usuarios
user_get_parser = generic_get_parser.copy()
user_get_parser.add_argument(
    "login",
    type=str,
    location="args",
    store_missing=False,
)

user_get_parser.add_argument(
    "name",
    type=str,
    location="args",
    store_missing=False,
)

user_get_parser.add_argument(
    "lastname",
    type=str,
    location="args",
    store_missing=False,
)

user_get_parser.add_argument(
    "user_type",
    type=str,
    location="args",
    store_missing=False,
)

user_get_parser.add_argument(
    "role_id",
    type=int,
    location="args",
    store_missing=False,
)

user_get_parser.add_argument(
    "sort_by",
    type=str,
    location="args",
    choices=["id", "login", "name", "lastname", "user_type", "role_id"],
    default=None,
)
