from typing import List, Union

from sqlalchemy import Row

from app.models import Reservation
from app.repository.base import BaseRepository
from app.repository.filters.reservation import ReservationFilter


class ReservationRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(ReservationRepository, self).__init__(*args, **kwargs)
        self.model = Reservation
        self.model_filter = kwargs.get('model_filter') or ReservationFilter()

    @staticmethod
    def object_mapping(rows: Union[Row, List[Row]]):
        from app.schemas.reservation import ReservationOutput

        if isinstance(rows, list):
            return [ReservationOutput(**row.__dict__) for row in rows]
        return ReservationOutput(**rows.__dict__)
