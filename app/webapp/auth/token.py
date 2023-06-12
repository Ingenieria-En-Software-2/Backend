from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

def generate_token(email):
    serializer = URLSafeTimedSerializer("fkslkfsdlksadacsfas")
    return serializer.dumps(email, salt="fkslkfsdlksadacsfas")


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer("fkslkfsdlksadacsfas")
    try:
        email = serializer.loads(
            token, salt="fkslkfsdlksadacsfas", max_age=expiration
        )
        return email
    except Exception:
        return False

def create_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="pruebasoswer2@gmail.com"
    )
    return msg
