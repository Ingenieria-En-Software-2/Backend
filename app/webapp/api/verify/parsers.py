from flask_restful import reqparse
from ..generic.parsers import generic_get_parser

verify_post_parser = reqparse.RequestParser()
verify_post_parser.add_argument(
    "id",
    type=int,
    required=True,
    help="id is required",
    location=("json", "values"),
)
verify_put_parser = reqparse.RequestParser()
verify_put_parser.add_argument("description", type=str, location=("json", "values"))

verify_get_parser = generic_get_parser.copy()
verify_get_parser.add_argument(
    "id",
    type=int,
    location="args",
    store_missing=False,
)

verify_get_parser.add_argument(
    "sort_by", type=int, location="args", choices=["id"], default=None
)
