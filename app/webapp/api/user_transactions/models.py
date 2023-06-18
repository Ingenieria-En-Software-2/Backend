from ... import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


class Currency(db.Model):
    __tablename__ = "currency"

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    symbol = db.Column(db.String())
    code = db.Column(db.String())

    def __init__(
        self,
        name,
        symbol,
        code
    ):
        self.name = name
        self.symbol = symbol
        self.code = code

    def __repr__(self):
        return "<Currency id {}>".format(self.id)


class TransactionStatus(db.Model):
    __tablename__ = "transaction_status"

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(
        self,
        name,
    ):
        self.name = name

    def __repr__(self):
        return "<TransactionStatus id {}>".format(self.id)


class UserTransaction(db.Model):
    __tablename__ = "user_transaction"

    user = relationship("User", cascade="delete")
    currency = relationship("Currency", cascade="delete")
    transaction_status = relationship("TransactionStatus", cascade="delete")
    user_accounts = relationship("UserAccount", cascade="delete",
    primaryjoin="UserTransaction.origin_account == UserAccount.id or UserTransaction.destination_account == UserAccount.id")

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="cascade"))
    origin_account = db.Column(db.Integer, db.ForeignKey(
        "user_account.id", ondelete="cascade"))
    destination_account = db.Column(db.Integer, db.ForeignKey(
        "user_account.id", ondelete="cascade"))
    amount = db.Column(db.Float())
    transaction_type = db.Column(db.String())
    transaction_date = db.Column(db.Date())
    transaction_description = db.Column(db.Text())
    currency_id = db.Column(db.Integer, db.ForeignKey(
        "currency.id", ondelete="cascade"))
    transaction_status_id = db.Column(db.Integer, db.ForeignKey(
        "transaction_status.id", ondelete="cascade"))

    def __init__(
        self,
        user_id,
        origin_account,
        destination_account,
        amount,
        transaction_type,
        transaction_date,
        transaction_description,
        currency_id,
        transaction_status_id
    ):
        self.user_id = user_id
        self.origin_account = origin_account
        self.destination_account = destination_account
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date
        self.transaction_description = transaction_description
        self.currency_id = currency_id
        self.transaction_status_id = transaction_status_id

    def __repr__(self):
        return "<UserTransaction id {}>".format(self.id)
