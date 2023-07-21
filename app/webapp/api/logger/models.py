from ... import db
from datetime import datetime


class LogEvent(db.Model):
    __tablename__ = "log_event"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    occurrence_time = db.Column(db.DateTime())
    description = db.Column(db.String())

    def __init__(self, **kwargs):
        super(LogEvent, self).__init__(**kwargs)
        self.occurrence_time = datetime.now()

    def __repr__(self):
        return "<AccountType id {}>".format(self.id)
