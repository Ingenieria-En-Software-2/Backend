from marshmallow import ValidationError


class CrudRepository:
    """
    A repository that provides basic CRUD (Create, Read, Update, Delete) operations for a given model.

    :param model: The SQLAlchemy model class to use for the repository.
    :param db: The SQLAlchemy database object to use for the repository.
    """

    def __init__(self, model, db, schema_create, schema_update):
        """
        Initializes a new instance of the `CrudRepository` class.

        :param model: The SQLAlchemy model class to use for the repository.
        :param db: The SQLAlchemy database object to use for the repository.
        :param schema_create: Marshmallow schema for validations
        :param schema_update: Marshmallow schema for validations
        """
        self.model = model
        self.db = db
        self.schema_create = schema_create
        self.schema_update = schema_update

    def get_all(self, page=1, per_page=None, sort_by=None, sort_order="asc", **kwargs):
        """
        Gets all records from the model.

        :param page: The page number to retrieve, or `1` to retrieve the first one.
        :param per_page: The number of records per page, or `None` to retrieve all records.
        :param sort_by: The name of the attribute to sort by, or `None` to not sort the records.
        :param sort_order: The sort order, 'desc' for descending or ascending by default.
        :param kwargs: The filter criteria to use for the query.
        :return: A list or a `QueryPagination` object containing all the records.
        """
        query = self.db.session.query(self.model)
        if kwargs is not None:
            checkAttributes(self.model, **kwargs)
            query = query.filter_by(**kwargs)

        if sort_by is not None:
            checkAttributes(self.model, **{sort_by: None})
            if sort_order != "desc":
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
        Gets a record from the model by ID.

        :param id: The ID of the record to retrieve.
        :return: The record with the specified ID, or `None` if no record was found.
        """
        return self.db.session.query(self.model).get(id)

    def get_by(self, **kwargs):
        """
        Gets records from the model that match the given filter criteria.

        :param kwargs: The filter criteria to use for the query.
        :return: The list of matching records.
        """
        checkAttributes(self.model, **kwargs)
        query = self.model.query.filter_by(**kwargs)
        return query.all()

    def create(self, **kwargs):
        """
        Creates a new record in the model.

        :param kwargs: The keyword arguments to use to create the new record.
        :return: The newly created record.
        """
        checkAttributes(self.model, **kwargs)

        # Validate the data

        result = self.schema_create().load(kwargs)


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
        Updates an existing record in the model.

        :param id: The ID of the record to update.
        :param kwargs: The keyword arguments to use to update the record.
        :return: The updated record.
        """
        checkAttributes(self.model, **kwargs)
        try:
            result = self.schema_update().load(kwargs)
        except ValidationError as err:
            print(err.messages)
            return None

        instance = self.get_by_id(id)
        if instance is None:
            raise ValueError(f"No record found with id {id}")
        try:
            for key, value in kwargs.items():
                # Check if the attribute is unique
                if hasattr(self.model, key):
                    column = getattr(self.model, key)
                    if column.unique:
                        raise ValueError(f"Cannot update unique attribute '{key}'")
                setattr(instance, key, value)
            self.db.session.commit()
            return instance
        except Exception as e:
            print(f"An error occurred while updating the record: {e}")
            self.db.session.rollback()
            return None

    def delete(self, id):
        """
        Deletes a record from the model. Given an id.

        :param id: Id of the record to delete.
        :return: The number of records remaining in the model. -1 if an error occurred.
        :raises ValueError: If no record was found with the specified ID.
        """
        instance = self.get_by_id(id)
        # Prevent from deleting a record that does not exist
        if instance is None:
            raise ValueError(f"No record found with id {id}")

        try:
            self.db.session.delete(instance)
            self.db.session.commit()
            # Return the number of elements remaining in the model
            return self.db.session.query(self.model).count()
        except Exception as e:
            print(f"An error occurred while deleting the record: {e}")
            self.db.session.rollback()
            return -1

    def exists(self, **kwargs):
        """
        Checks if a record exists in the model.

        :param kwargs: The keyword arguments to use to check if the record exists.
        :return: `True` if a record exists with the specified criteria, `False` otherwise.
        """
        checkAttributes(self.model, **kwargs)
        return self.db.session.query(self.model).filter_by(**kwargs).first() is not None


def checkAttributes(obj, **kwargs):
    for key in kwargs.keys():
        if not hasattr(obj, key):
            raise AttributeError(f"{key} is not an attribute of {obj.__name__}")
