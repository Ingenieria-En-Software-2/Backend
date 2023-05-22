from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'login',
    type=str,
    required=True,
    help="login is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'first_name',
    type=str,
    required=True,
    help="first_name is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'last_name',
    type=str,
    help="first_name is required",
    location=('json', 'values')
)

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument(
    'login',
    type=str,
    location=('json', 'values')
)

user_put_parser.add_argument(
    'first_name',
    type=str,
    location=('json', 'values')
)

user_put_parser.add_argument(
    'last_name',
    type=str,
    location=('json', 'values')
)