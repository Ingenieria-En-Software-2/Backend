from flask_restful import reqparse

role_post_parser = reqparse.RequestParser()
role_post_parser.add_argument(
    'description',
    type=str,
    required=True,
    help="login is required",
    location=('json', 'values')
)


role_put_parser = reqparse.RequestParser()
role_put_parser.add_argument(
    'description',
    type=str,
    location=('json', 'values')
)
