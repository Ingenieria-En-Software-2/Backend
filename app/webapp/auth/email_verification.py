from flask import url_for, render_template
from flask_mail import Message, Mail
from ..auth.token import generate_token


def create_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender="Caribbean Wallet")
    return msg


def send_verification_email(recipient: str):
    mail = Mail()
    token = generate_token(recipient)
    confirm_url = url_for("auth.verify_api", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    email = create_email(recipient, "Confirm your email", html)

    try:
        mail.send(email)
        print("Email de confirmación enviado.")
    except:
        pass
