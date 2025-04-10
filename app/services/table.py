
from sqlalchemy.orm import Session

from app.repository.table import TableRepository
from app.services.base import BaseService


class TableService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(TableService, self).__init__(session, *args, **kwargs)
        self.repository = TableRepository(session)
