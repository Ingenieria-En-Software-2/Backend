from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CrudRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return db.session.query(self.model).all()

    def get_by_id(self, id):
        return db.session.query(self.model).get(id)

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()

    def exists(self, **kwargs):
        return db.session.query(self.model).filter_by(**kwargs).first() is not None