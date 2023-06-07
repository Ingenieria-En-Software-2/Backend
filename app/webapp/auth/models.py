from .. import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

id_str = "<id {}>"


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    user_type = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

    def __init__(self, login, password, name, lastname, user_type, role_id):
        self.login = login
        self.password = password
        self.name = name
        self.lastname = lastname
        self.user_type = user_type
        self.role_id = role_id

    def __repr__(self):
        return id_str.format(self.id)


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return id_str.format(self.id)
