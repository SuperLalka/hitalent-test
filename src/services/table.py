
from sqlalchemy.orm import Session

from src.repository.table import TableRepository
from src.services.base import BaseService


class TableService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(TableService, self).__init__(*args, **kwargs)
        self.repository = TableRepository(session)
