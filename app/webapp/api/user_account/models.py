from ... import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


class AccountAffiliates(db.Model):
    __tablename__ = "account_affiliates"

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("account.id", ondelete="cascade"))
    affiliate_id = db.Column(
        db.Integer, db.ForeignKey("account.id", ondelete="cascade")
    )
    alias = db.Column(db.String())

    def __init__(self, account_id, affiliate_id, alias):
        self.account_id = account_id
        self.affiliate_id = affiliate_id
        self.alias = alias

    def __repr__(self):
        return "<AccountAffiliates id {}>".format(self.id)


class AccountType(db.Model):
    """
    Account Type:
    1. Current Account
    2. Savings Account
    """

    __tablename__ = "account_type"

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(
        self,
        name,
    ):
        self.name = name

    def __repr__(self):
        return "<AccountType id {}>".format(self.id)


class UserAccount(db.Model):
    __tablename__ = "account"

    user = relationship("User")
    account_type = relationship("AccountType")

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="cascade"))
    account_number = db.Column(db.String(20))
    account_type_id = db.Column(
        db.Integer, db.ForeignKey("account_type.id", ondelete="cascade")
    )

    def __init__(
        self,
        user_id,
        account_number,
        account_type_id,
    ):
        # Personal Data
        self.user_id = user_id
        self.account_number = account_number
        self.account_type_id = account_type_id

    def __repr__(self):
        return "<Account id {}>".format(self.id)


class UserAffiliates(db.Model):
    __tablename__ = "user_affiliates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="cascade"))
    document_number = db.Column(db.String(20))
    name = db.Column(db.String())
    phone = db.Column(db.String())
    mail = db.Column(db.String())
    wallet = db.Column(db.String())

    def __init__(
        self,
        user_id,
        document_number,
        name,
        phone,
        mail,
        wallet,
    ):
        self.user_id = user_id
        self.document_number = document_number
        self.name = name
        self.phone = phone
        self.mail = mail
        self.wallet = wallet
