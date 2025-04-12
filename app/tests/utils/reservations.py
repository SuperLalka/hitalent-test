import datetime

from faker import Faker
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models import Reservation
from app.repository.reservation import ReservationRepository
from app.schemas.reservation import ReservationInput

fake = Faker()


async def create_reservation(
        db: Session,
        table_id: int,
        customer_name: str = None,
        duration_minutes: int = None,
) -> Reservation:
    return await ReservationRepository(db).create(
        ReservationInput(
            customer_name=customer_name or fake.name(),
            reservation_time=datetime.datetime.strftime(
                fake.future_datetime(end_date='+30d'), settings.DATETIME_PATTERN
            ),
            duration_minutes=duration_minutes or fake.random_int(30, 600),
            table_id=table_id
        )
    )
