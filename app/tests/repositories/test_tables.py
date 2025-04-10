import random

from faker import Faker
from sqlalchemy.orm import Session

from app.repository.table import TableRepository
from app.schemas.table import TableInput
from app.tests.factories import TableFactory
from app.tests.fixtures import LOCATIONS_EXAMPLES


async def test_create(db: Session, faker: Faker) -> None:
    new_table_data = {
        "name": faker.word(),
        "seats": faker.random_int(1, 6),
        "location": faker.random_element(LOCATIONS_EXAMPLES),
    }

    table_in = TableInput(**new_table_data)
    table = await TableRepository(db).create(table_in)
    assert table.name == new_table_data['name']
    assert table.seats == new_table_data['seats']
    assert table.location == new_table_data['location']


async def test_exists_by_id(db: Session) -> None:
    table = TableFactory()
    assert await TableRepository(db).exists_by_id(table.id)


# TODO: need filter
async def test_is_exists(db: Session) -> None:
    table_factory = TableFactory()
    assert await TableRepository(db).is_exists()


async def test_get_all(db: Session) -> None:
    tables_num = random.randint(3, 6)
    [TableFactory() for _ in range(tables_num)]

    tables = await TableRepository(db).get_all()
    assert tables.count() == tables_num


async def test_get_by_id(db: Session) -> None:
    table_factory = TableFactory()
    table = await TableRepository(db).get_by_id(table_factory.id)

    assert table.id == table_factory.id
    assert table.name == table_factory.name
    assert table.seats == table_factory.seats
    assert table.location == table_factory.location


async def test_update(db: Session, faker: Faker) -> None:
    table_factory = TableFactory()

    new_table_data = {
        "name": faker.word(),
        "seats": faker.random_int(1, 6),
        "location": faker.random_element(LOCATIONS_EXAMPLES),
    }

    assert table_factory.name != new_table_data['name']
    assert table_factory.seats != new_table_data['seats']
    assert table_factory.location != new_table_data['location']

    await TableRepository(db).update(table_factory.id, new_table_data)

    assert table_factory.name == new_table_data['name']
    assert table_factory.seats == new_table_data['seats']
    assert table_factory.location == new_table_data['location']


async def test_delete(db: Session) -> None:
    table_factory = TableFactory()
    await TableRepository(db).delete(table_factory.id)

    assert not await TableRepository(db).exists_by_id(table_factory.id)
