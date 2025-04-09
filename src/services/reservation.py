
from sqlalchemy.orm import Session

from src.repository.reservation import ReservationRepository
from src.services.base import BaseService


class ReservationService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(ReservationService, self).__init__(*args, **kwargs)
        self.repository = ReservationRepository(session)
