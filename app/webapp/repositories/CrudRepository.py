class CrudRepository:
    """
    A repository that provides basic CRUD (Create, Read, Update, Delete) operations for a given model.

    :param model: The SQLAlchemy model class to use for the repository.
    :param db: The SQLAlchemy database object to use for the repository.
    """

    def __init__(self, model, db):
        """
        Initializes a new instance of the `CrudRepository` class.

        :param model: The SQLAlchemy model class to use for the repository.
        :param db: The SQLAlchemy database object to use for the repository.
        """
        self.model = model
        self.db = db

    def get_all(self, page=1, per_page=None, sort_by=None, sort_order='asc'):
        """
        Gets all records from the repository.

        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :return: A list or a `QueryPagination` object containing all the records.
        """
        query = self.db.session.query(self.model)

        if sort_by is not None:
            if sort_order != 'desc':
                query = query.order_by(getattr(self.model, sort_by).asc())
            else:
                query = query.order_by(getattr(self.model, sort_by).desc())

        if per_page is not None:
            # Error out is false to return empty list instead of 404 error when page is out of range
            records = query.paginate(page=page, per_page=per_page, error_out=False)
        else:
            records = query.all()

        return records

    def get_by_id(self, id):
        """
        Gets a record from the repository by ID.

        :param id: The ID of the record to retrieve.
        :return: The record with the specified ID, or `None` if no record was found.
        """
        return self.db.session.query(self.model).get(id)

    def create(self, **kwargs):
        """
        Creates a new record in the repository.

        :param kwargs: The keyword arguments to use to create the new record.
        :return: The newly created record.
        """
        try:
            instance = self.model(**kwargs)
            self.db.session.add(instance)
            self.db.session.commit()
            return instance
        except Exception as e:
            print(f"An error occurred while creating the record: {e}")
            self.db.session.rollback()
            return None

    def update(self, id, **kwargs):
        """
        Updates an existing record in the repository.

        :param id: The ID of the record to update.
        :param kwargs: The keyword arguments to use to update the record.
        :return: The updated record.
        """
        try:
            instance = self.get_by_id(id)
            if instance is None:
                return None
            
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.session.commit()
            return instance
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")
            self.db.session.rollback()
            return None

    def delete(self, id):
        """
        Deletes a record from the repository. Given an id.

        :param id: Id of the record to delete.
        :return: `True` if the record was deleted, `False` otherwise.
        """
        try:
            # Prevent from deleting a record that does not exist
            instance = self.get_by_id(id)
            if instance is None:
                return False

            self.db.session.delete(instance)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"An error occurred while deleting the record: {e}")
            self.db.session.rollback()
            return False

    def exists(self, **kwargs):
        """
        Checks if a record exists in the repository.

        :param kwargs: The keyword arguments to use to check if the record exists.
        :return: `True` if a record exists with the specified criteria, `False` otherwise.
        """
        return self.db.session.query(self.model).filter_by(**kwargs).first() is not None