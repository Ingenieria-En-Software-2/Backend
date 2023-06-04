from flask_restful import reqparse
from ..generic.parsers import generic_get_parser

role_post_parser = reqparse.RequestParser()
role_post_parser.add_argument(
    "description",
    type=str,
    required=True,
    help="login is required",
    location=("json", "values"),
)

role_put_parser = reqparse.RequestParser()
role_put_parser.add_argument("description", type=str, location=("json", "values"))

role_get_parser = generic_get_parser.copy()
role_get_parser.add_argument(
    "description",
    type=str,
    location="args",
    store_missing=False,
)

role_get_parser.add_argument(
    "sort_by", type=str, location="args", choices=["id", "description"], default=None
)
