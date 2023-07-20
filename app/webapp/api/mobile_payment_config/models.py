from ... import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


class MobilePaymentConfig(db.Model):
    __tablename__ = "mobile_payment_config"

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    email = db.Column(db.String())
    document = db.Column(db.String())
    receiver_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    max_amount = db.Column(db.Float())

    def __init__(
        self,
        user_id,
        email,
        document,
        receiver_name,
        phone_number,
        account_id,
        max_amount,
    ):
        """_summary_
        Args:
            user_id (int): Id of the user
            email (string): email of the mobile payment account holder
            document (string): document of the mobile payment account holder
            receiver_name (string): receiver_name of the mobile payment account holder
            phone_number (string): phone_number of the mobile payment account holder
            account_id (int): account_id of the mobile payment account holder
            max_amount (float): max_amount of the mobile payment account holder
        """
        self.user_id = user_id
        self.email = email  # Email of the mobile payment account holder
        self.document = document  # Document of mobile payment account holder
        self.receiver_name = receiver_name  # Name of mobile payment account holder
        self.phone_number = phone_number  # Phone number of mobile payment account holder
        self.account_id = account_id  # Account id of mobile payment account holder
        self.max_amount = max_amount  # Max amount of money that can be sent to the mobile payment account holder
        

    def __repr__(self):
        return "<MobilePaymentConfig id {}>".format(self.id)
