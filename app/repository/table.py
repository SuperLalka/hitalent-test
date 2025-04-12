from typing import List, Union

from sqlalchemy import Row

from app.models import Table
from app.repository.base import BaseRepository


class TableRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(TableRepository, self).__init__(*args, **kwargs)
        self.model = Table

    @staticmethod
    def object_mapping(rows: Union[Row, List[Row]]):
        from app.schemas.table import TableOutput

        if isinstance(rows, list):
            return [TableOutput(**row.__dict__) for row in rows]
        return TableOutput(**rows.__dict__)
