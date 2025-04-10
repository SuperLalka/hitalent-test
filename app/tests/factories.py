import datetime

import factory
from pytest_factoryboy import register

from app.models import Reservation, Table
from app.tests.fixtures import LOCATIONS_EXAMPLES


@register
class TableFactory(factory.Factory):
    class Meta:
        model = Table

    name = factory.Sequence(lambda n: 'Table {}'.format(n))
    seats = factory.Faker('random_int', min=1, max=6)
    location = factory.Faker('random_element', elements=LOCATIONS_EXAMPLES)


@register
class ReservationFactory(factory.Factory):
    class Meta:
        model = Reservation

    customer_name = factory.Faker('name', locale='ru_RU')
    reservation_time = factory.Faker('datetime', start_datetime=datetime.datetime.now())
    duration_minutes = factory.Faker('random_int', min=1, max=600)
    table_id = factory.Faker('random_int')
