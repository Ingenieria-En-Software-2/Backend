from flask_restful import reqparse
from ..generic.parsers import generic_get_parser


# Post Request
# User Data
account_holder_post_parser = reqparse.RequestParser()
account_holder_post_parser.add_argument(
    "login",
    type=str,
    required=True,
    help="login is required",
    location=("json", "values"),
)

account_holder_post_parser.add_argument(
    "password",
    type=str,
    required=False,
    help="account holder password",
    location=("json", "values"),
)

account_holder_post_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="name is required",
    location=("json", "values"),
)

account_holder_post_parser.add_argument(
    "lastname",
    type=str,
    required=True,
    help="lastname is required",
    location=("json", "values"),
)

account_holder_post_parser.add_argument(
    "user_type",
    type=str,
    required=True,
    help="user_type is required",
    location=("json", "values"),
)

account_holder_post_parser.add_argument(
    "role_id",
    type=int,
    required=True,
    help="role_id is required",
    location=("json", "values"),
)

# Personal Data
account_holder_post_parser.add_argument(
    "identification_document",
    type=str,
    required=True,
    help="identification_document is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "gender",
    type=str,
    required=True,
    help="gender is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "civil_status",
    type=str,
    required=True,
    help="civil_status is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "birthdate",
    type=str,
    required=True,
    help="birthdate is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "phone",
    type=str,
    required=True,
    help="phone is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "nacionality",
    type=str,
    required=True,
    help="nacionality is required",
    location=("json", "values"),
)

# Residence Address

account_holder_post_parser.add_argument(
    "street",
    type=str,
    required=True,
    help="street is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "sector",
    type=str,
    required=True,
    help="sector is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "city",
    type=str,
    required=True,
    help="city is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "country",
    type=str,
    required=True,
    help="country is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "province",
    type=str,
    required=True,
    help="province is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "township",
    type=str,
    required=True,
    help="township is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "address",
    type=str,
    required=True,
    help="address is required",
    location=("json", "values"),
)

# Employer data
account_holder_post_parser.add_argument(
    "employer_name",
    type=str,
    required=True,
    help="employer_name is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_rif",
    type=str,
    required=True,
    help="employer_rif is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_phone",
    type=str,
    required=True,
    help="employer_phone is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_city",
    type=str,
    required=True,
    help="employer_city is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_country",
    type=str,
    required=True,
    help="employer_country is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_province",
    type=str,
    required=True,
    help="employer_province is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_township",
    type=str,
    required=True,
    help="employer_township is required",
    location=("json", "values"),
)
account_holder_post_parser.add_argument(
    "employer_address",
    type=str,
    required=True,
    help="employer_address is required",
    location=("json", "values"),
)

# Put Request
account_holder_put_parser = reqparse.RequestParser()
# User Data
account_holder_put_parser.add_argument(
    "login",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

account_holder_put_parser.add_argument(
    "password",
    type=str,
    required=False,
    store_missing=False,
    location=("json", "values"),
)

account_holder_put_parser.add_argument(
    "name",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

account_holder_put_parser.add_argument(
    "lastname",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

account_holder_put_parser.add_argument(
    "user_type",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

account_holder_put_parser.add_argument(
    "role_id",
    type=int,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

# Personal Data
account_holder_put_parser.add_argument(
    "identification_document",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "gender",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "civil_status",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "birthdate",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "phone",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "nacionality",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

# Residence Address

account_holder_put_parser.add_argument(
    "street",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "sector",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "city",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "country",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "province",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "township",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "address",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

# Employer data
account_holder_put_parser.add_argument(
    "employer_name",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_rif",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_phone",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_city",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_country",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_province",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_township",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)
account_holder_put_parser.add_argument(
    "employer_address",
    type=str,
    required=True,
    store_missing=False,
    location=("json", "values"),
)

# Get Requests  TODO: Verify needed search fields
account_holder_get_parser = generic_get_parser.copy()


# Personal Data
account_holder_get_parser.add_argument(
    "identification_document",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "gender",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "civil_status",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "birthdate",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "phone",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "nacionality",
    type=str,
    store_missing=False,
    location=("args"),
)

# Residence Address

account_holder_get_parser.add_argument(
    "street",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "sector",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "city",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "country",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "province",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "township",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "address",
    type=str,
    store_missing=False,
    location=("args"),
)

# Employer data
account_holder_get_parser.add_argument(
    "employer_name",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_rif",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_phone",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_city",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_country",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_province",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_township",
    type=str,
    store_missing=False,
    location=("args"),
)
account_holder_get_parser.add_argument(
    "employer_address",
    type=str,
    store_missing=False,
    location=("args"),
)


account_holder_get_parser.add_argument(
    "sort_by",
    type=str,
    location="args",
    choices=["id", "login", "name", "lastname", "user_type", "role_id"],
    default=None,
)
