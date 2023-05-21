from flask_sqlalchemy import SQLAlchemy
from webapp.repositories.CrudRepository import CrudRepository

db = SQLAlchemy()

class PagingAndSortingRepository(CrudRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_all(self, page=1, per_page=10, sort_by=None, sort_order='asc'):
        query = db.session.query(self.model)
        if sort_by is not None:
            if sort_order == 'asc':
                query = query.order_by(sort_by)
            else:
                query = query.order_by(db.desc(sort_by))
        # Error out is false to return empty list instead of 404 error when page is out of range
        return query.paginate(page=page, per_page=per_page, error_out=False)
