import random

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.reservation import ReservationRepository
from app.tests.factories import ReservationFactory


def test_get_all_reservations(client: TestClient) -> None:
    reservations_num = random.randint(3, 6)
    [ReservationFactory() for _ in range(reservations_num)]

    response = client.get(f"{settings.API_V1_STR}/reservations/")
    assert response.status_code == 200

    content = response.json()
    assert len(content["data"]) == reservations_num


def test_create_reservation(client: TestClient, faker: Faker, db: Session) -> None:
    data = {
        "customer_name": faker.name(),
        "reservation_time": faker.future_datetime(end_date='+1y'),
        "duration_minutes": faker.random_int(30, 600),
        "table_id": 1,
    }
    response = client.post(
        f"{settings.API_V1_STR}/reservations/",
        json=data,
    )
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["customer_name"] == data["customer_name"]
    assert content["reservation_time"] == data["reservation_time"]
    assert content["duration_minutes"] == data["duration_minutes"]
    assert content["table_id"] == data["table_id"]

    assert ReservationRepository(db).exists_by_id(content['id'])


def test_delete_reservation(client: TestClient, db: Session) -> None:
    reservation = ReservationFactory()
    response = client.delete(
        f"{settings.API_V1_STR}/reservations/{reservation.id}",
    )
    assert response.status_code == 200

    content = response.json()
    assert content["message"] == "Object deleted successfully"

    assert not ReservationRepository(db).exists_by_id(reservation.id)


def test_delete_reservation_not_found(client: TestClient) -> None:
    fake_reservation_id = random.randint(1, 100)
    response = client.delete(
        f"{settings.API_V1_STR}/reservations/{fake_reservation_id}",
    )
    assert response.status_code == 404

    content = response.json()
    assert content["detail"] == "Object not found"
