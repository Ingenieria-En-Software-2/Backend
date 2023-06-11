from flask_restful import reqparse
from ..generic.parsers import generic_get_parser

verify_post_parser = reqparse.RequestParser()
verify_post_parser.add_argument('token')

verify_put_parser = reqparse.RequestParser()
verify_put_parser.add_argument('token')

verify_get_parser = generic_get_parser.copy()
verify_get_parser.add_argument('token')
