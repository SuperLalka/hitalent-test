
import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session

from app.config.database import engine
from app.models import Reservation, Table
from app.tests.fixtures import LOCATIONS_EXAMPLES

session = Session(engine)


class TableFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Table
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Sequence(lambda n: 'Table {}'.format(n))
    seats = factory.Faker('random_int', min=1, max=5)
    location = factory.Faker('random_element', elements=LOCATIONS_EXAMPLES)


class ReservationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Reservation
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    customer_name = factory.Faker('name', locale='ru_RU')
    reservation_time = factory.Faker('future_date', end_date='+30d')
    duration_minutes = factory.Faker('random_int', min=1, max=600)
    table = factory.SubFactory(TableFactory)
