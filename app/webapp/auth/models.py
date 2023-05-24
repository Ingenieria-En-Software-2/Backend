from .. import db
import jwt, datetime

id_str = '<id {}>'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String())
    password = db.Column(db.String())
    name = db.Column(db.String())
    lastname = db.Column(db.String())
    user_type = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, login, password, name, lastname, user_type, role_id):
        self.login = login
        self.password = password
        self.name = name
        self.lastname = lastname
        self.user_type = user_type
        self.role_id = role_id

    def __repr__(self):
        return id_str.format(self.id)
    
    def encode_token(self, id, role_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': id,
            'role': role_id
        }

        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256')
    
    @staticmethod
    def decode_token(token):
        try: 
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub'], payload['role']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return id_str.format(self.id)
