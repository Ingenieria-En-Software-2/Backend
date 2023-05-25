from flask_restful import reqparse

generic_get_parser = reqparse.RequestParser()

generic_get_parser.add_argument("page_number", type=int, location="args", default=1)

generic_get_parser.add_argument(
    "page_size",
    type=int,
    location="args",
    default=10,
)

generic_get_parser.add_argument(
    "sort_order", type=str, location="args", choices=["asc", "desc"], default="asc"
)
