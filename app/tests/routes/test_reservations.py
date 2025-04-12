import datetime
import random
import uuid

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.reservation import ReservationRepository
from app.tests.factories import ReservationFactory, TableFactory
from app.tests.utils.reservations import create_reservation


async def test_get_all_reservations(client: TestClient, db: Session, table: TableFactory) -> None:
    reservations_num = random.randint(3, 6)
    [await create_reservation(db, table_id=table.id) for _ in range(reservations_num)]

    response = client.get(f"{settings.API_V1_STR}/reservations/")
    assert response.status_code == 200

    content = response.json()
    assert len(content) == reservations_num


async def test_create_reservation(
        client: TestClient,
        faker: Faker,
        db: Session,
        table: TableFactory
) -> None:
    data = {
        "customer_name": faker.name(),
        "reservation_time": datetime.datetime.strftime(
            faker.future_datetime(end_date='+30d'), settings.DATETIME_PATTERN
        ),
        "duration_minutes": faker.random_int(30, 600),
        "table_id": table.id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/reservations/",
        json=data,
    )
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["customer_name"] == data["customer_name"]
    assert (
        datetime.datetime.strptime(content["reservation_time"], settings.DATETIME_PATTERN)
        == datetime.datetime.strptime(data["reservation_time"], settings.DATETIME_PATTERN)
    )
    assert content["duration_minutes"] == data["duration_minutes"]
    assert content["table_id"] == data["table_id"]

    assert await ReservationRepository(db).exists_by_id(content['id'])


async def test_delete_reservation(client: TestClient, db: Session, reservation: ReservationFactory) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/reservations/{reservation.id}",
    )
    assert response.status_code == 204

    assert not await ReservationRepository(db).exists_by_id(reservation.id)


async def test_delete_reservation_not_found(client: TestClient) -> None:
    fake_reservation_id = uuid.uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/reservations/{fake_reservation_id}",
    )
    assert response.status_code == 404

    content = response.json()
    assert content["detail"] == "Object not found"
