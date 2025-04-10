import random

from faker import Faker
from sqlalchemy.orm import Session

from app.repository.filters.reservation import ReservationFilter
from app.repository.reservation import ReservationRepository
from app.schemas.reservation import ReservationInput
from app.tests.factories import ReservationFactory


async def test_create(db: Session, faker: Faker) -> None:
    new_reservation_data = {
        "customer_name": faker.name(),
        "reservation_time": faker.future_datetime(end_date='+1y'),
        "duration_minutes": faker.random_int(30, 600),
        "table_id": 1,
    }

    reservation_in = ReservationInput(**new_reservation_data)
    reservation = await ReservationRepository(db).create(reservation_in)
    assert reservation.customer_name == new_reservation_data['customer_name']
    assert reservation.reservation_time == new_reservation_data['reservation_time']
    assert reservation.duration_minutes == new_reservation_data['duration_minutes']


async def test_exists_by_id(db: Session) -> None:
    reservation = ReservationFactory()
    assert await ReservationRepository(db).exists_by_id(reservation.id)


async def test_is_exists(db: Session) -> None:
    reservation_factory = ReservationFactory()
    assert await ReservationRepository(db, filter=ReservationFilter(
        customer_name=reservation_factory.customer_name,
    )).is_exists()


async def test_get_all(db: Session) -> None:
    reservations_num = random.randint(3, 6)
    [ReservationFactory() for _ in range(reservations_num)]

    reservations = await ReservationRepository(db).get_all()
    assert reservations.count() == reservations_num


async def test_get_all_with_filter(db: Session, faker: Faker) -> None:
    customer_name = faker.name()
    table_id = faker.random_int(1, 10)

    ReservationFactory(customer_name=customer_name, table_id=faker.random_int(11, 20))
    ReservationFactory(customer_name=customer_name, table_id=faker.random_int(11, 20))
    ReservationFactory(customer_name=customer_name, table_id=table_id)
    ReservationFactory(customer_name=faker.prefix() + faker.name(), table_id=table_id)
    ReservationFactory(customer_name=faker.prefix() + faker.name(), table_id=table_id)

    result = await ReservationRepository(
        db,
        filter=ReservationFilter(
            customer_name=customer_name,
        )
    ).get_all()
    assert result.count() == 3

    result = await ReservationRepository(
        db,
        filter=ReservationFilter(
            table_id=table_id,
        )
    ).get_all()
    assert result.count() == 3

    result = await ReservationRepository(
        db,
        filter=ReservationFilter(
            customer_name=customer_name,
            table_id=table_id,
        )
    ).get_all()
    assert result.count() == 1


async def test_get_by_id(db: Session) -> None:
    reservation_factory = ReservationFactory()
    reservation = await ReservationRepository(db).get_by_id(reservation_factory.id)

    assert reservation.id == reservation_factory.id
    assert reservation.customer_name == reservation_factory.customer_name
    assert reservation.reservation_time == reservation_factory.reservation_time
    assert reservation.duration_minutes == reservation_factory.duration_minutes


async def test_update(db: Session, faker: Faker) -> None:
    reservation_factory = ReservationFactory()

    new_reservation_data = {
        "customer_name": faker.name(),
        "reservation_time": faker.future_datetime(end_date='+1y'),
        "duration_minutes": faker.random_int(30, 600),
    }

    assert reservation_factory.name != new_reservation_data['name']
    assert reservation_factory.seats != new_reservation_data['seats']
    assert reservation_factory.location != new_reservation_data['location']

    await ReservationRepository(db).update(reservation_factory.id, new_reservation_data)

    assert reservation_factory.name == new_reservation_data['name']
    assert reservation_factory.seats == new_reservation_data['seats']
    assert reservation_factory.location == new_reservation_data['location']


async def test_delete(db: Session) -> None:
    reservation_factory = ReservationFactory()
    await ReservationRepository(db).delete(reservation_factory.id)

    assert not await ReservationRepository(db).exists_by_id(reservation_factory.id)
