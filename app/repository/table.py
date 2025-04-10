
from app.models import Table
from app.repository.base import BaseRepository


class TableRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(TableRepository, self).__init__(*args, **kwargs)
        self.model = Table
