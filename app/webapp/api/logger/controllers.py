"""
Module containing the definition of the AccountHolderApi class, which inherits from the
CrudApi class, and is in charge of handling HTTP requests related to account holders.
"""



from ...auth.models import db
from ...api.generic.CrudApi import CrudApi
from webapp.repositories.CrudRepository import CrudRepository
from ...api.logger.models import LogEvent
from .schemas import (
    Create_Log_Event_Schema,
    Update_Log_Event_Schema,
    Get_Log_Event_Schema,
)

# Instance of the account holder repository
logger_repository = CrudRepository(LogEvent, db, Create_Log_Event_Schema, Update_Log_Event_Schema)


class Log_EventApi(CrudApi):
    # Call to the base class constructor CrudApi
    def __init__(self):
        super().__init__(
            logger_repository,  # Repositorio de usuarios
            Get_Log_Event_Schema,  # Esquema Get para roles
        )
