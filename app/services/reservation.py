
from sqlalchemy.orm import Session

from app.repository.reservation import ReservationRepository
from app.services.base import BaseService


class ReservationService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(ReservationService, self).__init__(session, *args, **kwargs)
        self.repository = ReservationRepository(session)
