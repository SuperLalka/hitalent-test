import datetime
import random

from faker import Faker
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.filters.reservation import ReservationFilter
from app.repository.reservation import ReservationRepository
from app.schemas.reservation import ReservationInput, ReservationUpdate
from app.tests.factories import ReservationFactory, TableFactory
from app.tests.utils.reservations import create_reservation
from app.tests.utils.tables import create_table


async def test_create_reservation(db: Session, faker: Faker, table: TableFactory) -> None:
    new_reservation_data = {
        "customer_name": faker.name(),
        "reservation_time": datetime.datetime.strftime(
            faker.future_datetime(end_date='+30d'), settings.DATETIME_PATTERN
        ),
        "duration_minutes": faker.random_int(30, 600),
        "table_id": table.id,
    }

    reservation_in = ReservationInput(**new_reservation_data)
    reservation = await ReservationRepository(db).create(reservation_in)
    assert reservation.customer_name == new_reservation_data['customer_name']
    assert (
        datetime.datetime.strftime(reservation.reservation_time, settings.DATETIME_PATTERN)
        == new_reservation_data['reservation_time']
    )
    assert reservation.duration_minutes == new_reservation_data['duration_minutes']


async def test_exists_by_id_reservation(db: Session, reservation: ReservationFactory) -> None:
    assert await ReservationRepository(db).exists_by_id(reservation.id)


async def test_is_exists_reservation(db: Session, reservation: ReservationFactory) -> None:
    assert await ReservationRepository(db, model_filter=ReservationFilter(
        customer_name=reservation.customer_name,
    )).is_exists()


async def test_get_all_reservation(db: Session) -> None:
    reservations_num = random.randint(3, 6)
    table = await create_table(db)
    [await create_reservation(db, table_id=table.id) for _ in range(reservations_num)]

    reservations = await ReservationRepository(db).get_all()
    assert len(reservations) == reservations_num


async def test_get_all_with_filter_reservation(db: Session, faker: Faker) -> None:
    customer_name = faker.name()
    table_one = await create_table(db)
    table_two = await create_table(db)

    await create_reservation(db, customer_name=customer_name, table_id=table_one.id)
    await create_reservation(db, customer_name=customer_name, table_id=table_one.id)
    await create_reservation(db, customer_name=customer_name, table_id=table_two.id)
    await create_reservation(db, customer_name=faker.prefix() + faker.name(), table_id=table_two.id)
    await create_reservation(db, customer_name=faker.prefix() + faker.name(), table_id=table_two.id)

    result = await ReservationRepository(
        db,
        model_filter=ReservationFilter(
            customer_name=customer_name,
        )
    ).get_all()
    assert len(result) == 3

    result = await ReservationRepository(
        db,
        model_filter=ReservationFilter(
            table_id=table_one.id,
        )
    ).get_all()
    assert len(result) == 2

    result = await ReservationRepository(
        db,
        model_filter=ReservationFilter(
            customer_name=customer_name,
            table_id=table_two.id,
        )
    ).get_all()
    assert len(result) == 1


async def test_get_by_id_reservation(db: Session, reservation: ReservationFactory) -> None:
    reservation_obj = await ReservationRepository(db).get_by_id(reservation.id)

    assert reservation_obj.id == reservation.id
    assert reservation_obj.customer_name == reservation.customer_name
    assert reservation_obj.reservation_time == reservation.reservation_time
    assert reservation_obj.duration_minutes == reservation.duration_minutes


async def test_update_reservation(db: Session, faker: Faker) -> None:
    table = await create_table(db)
    reservation = await create_reservation(db, table_id=table.id)

    new_reservation_data = {
        "customer_name": faker.name(),
        "reservation_time": datetime.datetime.strftime(
            faker.future_datetime(end_date='+30d'), settings.DATETIME_PATTERN
        ),
        "duration_minutes": faker.random_int(30, 600),
    }
    reservation_update = ReservationUpdate(**new_reservation_data)

    assert reservation.customer_name != reservation_update.customer_name
    assert reservation.reservation_time != reservation_update.reservation_time
    assert reservation.duration_minutes != reservation_update.duration_minutes

    await ReservationRepository(db).update(reservation, reservation_update)

    assert reservation.customer_name == reservation_update.customer_name
    assert reservation.reservation_time == reservation_update.reservation_time
    assert reservation.duration_minutes == reservation_update.duration_minutes


async def test_delete_reservation(db: Session) -> None:
    table = await create_table(db)
    reservation = await create_reservation(db, table.id)

    await ReservationRepository(db).delete(reservation)

    assert not await ReservationRepository(db).exists_by_id(reservation.id)
