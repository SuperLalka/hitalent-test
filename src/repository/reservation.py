
from src.models import Reservation
from src.repository.base import BaseRepository
from src.repository.filters.reservation import ReservationFilter


class ReservationRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(ReservationRepository, self).__init__(*args, **kwargs)
        self.model = Reservation
        self.filter = ReservationFilter
