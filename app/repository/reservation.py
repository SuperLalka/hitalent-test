
from app.models import Reservation
from app.repository.base import BaseRepository
from app.repository.filters.reservation import ReservationFilter


class ReservationRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(ReservationRepository, self).__init__(*args, **kwargs)
        self.model = Reservation
        self.model_filter = ReservationFilter
