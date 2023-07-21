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
    email = create_email(recipient, "Confirma tu usuario", html)

    try:
        mail.send(email)
    except:
        pass


def send_transaction_email(recipient: str):
    mail = Mail()
    token = generate_token(recipient)
    confirm_url = url_for("auth.verify_api", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    email = create_email(recipient, "Confirma tu usuario", html)

    try:
        mail.send(email)
    except:
        pass


def send_transaction_email(type, recipient: str, origin, destination, amount, currency):
    mail = Mail()
    token = generate_token(recipient)
    if type == "inter_wallet":
        html = render_template(
            "transaction_email.html",
            type="Inter Wallet ",
            origin=origin,
            destination=destination,
            amount=amount,
            currency=currency,
        )
        email = create_email(
            recipient,
            "Se ha realizado una transferencia Inter Wallet desde tu cuenta",
            html,
        )
    else:
        html = render_template(
            "transaction_email.html",
            type="",
            origin=origin,
            destination=destination,
            amount=amount,
            currency=currency,
        )
        email = create_email(
            recipient, "Se ha realizado una transferencia desde tu cuenta", html
        )
    try:
        mail.send(email)
    except:
        pass


def send_pago_movil_email(recipient: str, origin, CI, Name, Wallet, amount, currency):
    mail = Mail()
    token = generate_token(recipient)
    html = render_template(
        "pago_movil_email.html",
        origin=origin,
        destCI=CI,
        destName=Name,
        wallet=Wallet,
        amount=amount,
        currency=currency,
    )
    email = create_email(
        recipient,
        "Se ha realizado una transferencia Pago Móvil de una de tus cuentas",
        html,
    )

    try:
        mail.send(email)
    except:
        pass
