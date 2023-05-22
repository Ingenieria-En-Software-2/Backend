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
    'password',
    type=str,
    required=True,
    help="login is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'name',
    type=str,
    required=True,
    help="name is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'lastname',
    type=str,
    required=True,
    help="lastname is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'user_type',
    type=str,
    required=True,
    help="user_type is required",
    location=('json', 'values')
)

user_post_parser.add_argument(
    'role_id',
    type=int,
    required=True,
    help="role_id is required",
    location=('json', 'values')
)

user_put_parser = reqparse.RequestParser()
user_put_parser.add_argument(
    'login',
    type=str,    
    help="login is required",
    location=('json', 'values')
)

user_put_parser.add_argument(
    'password',
    type=str,    
    help="login is required",
    location=('json', 'values')
)

user_put_parser.add_argument(
    'name',
    type=str,    
    help="name is required",
    location=('json', 'values')
)

user_put_parser.add_argument(
    'lastname',
    type=str,    
    help="lastname is required",
    location=('json', 'values')
)

user_put_parser.add_argument(
    'user_type',
    type=str,    
    help="user_type is required",
    location=('json', 'values')
)

user_put_parser.add_argument(
    'role_id',
    type=int,    
    help="role_id is required. Must be a int",
    location=('json', 'values')
)