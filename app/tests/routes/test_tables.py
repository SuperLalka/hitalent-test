import random

from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repository.table import TableRepository
from app.tests.fixtures import LOCATIONS_EXAMPLES
from app.tests.utils.tables import create_table


async def test_get_all_tables(client: TestClient, db: Session) -> None:
    tables_num = random.randint(3, 6)
    [await create_table(db) for _ in range(tables_num)]

    response = client.get(f"{settings.API_V1_STR}/tables/")
    assert response.status_code == 200

    content = response.json()
    assert len(content) == tables_num


async def test_create_table(client: TestClient, faker: Faker, db: Session) -> None:
    data = {
        "name": faker.word(),
        "seats": faker.random_int(1, 5),
        "location": faker.random_element(LOCATIONS_EXAMPLES),
    }
    response = client.post(
        f"{settings.API_V1_STR}/tables/",
        json=data,
    )
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["name"] == data["name"]
    assert content["seats"] == data["seats"]
    assert content["location"] == data["location"]

    assert await TableRepository(db).exists_by_id(content['id'])


async def test_delete_table(client: TestClient, db: Session) -> None:
    table = await create_table(db)
    response = client.delete(
        f"{settings.API_V1_STR}/tables/{table.id}",
    )
    assert response.status_code == 204

    assert not await TableRepository(db).exists_by_id(table.id)


async def test_delete_table_not_found(client: TestClient) -> None:
    fake_table_id = random.randint(1, 100)
    response = client.delete(
        f"{settings.API_V1_STR}/tables/{fake_table_id}",
    )
    assert response.status_code == 404

    content = response.json()
    assert content["detail"] == "Object not found"
