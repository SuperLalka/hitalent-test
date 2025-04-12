import random

from faker import Faker
from sqlalchemy.orm import Session

from app.repository.table import TableRepository
from app.schemas.table import TableInput
from app.tests.factories import TableFactory
from app.tests.fixtures import LOCATIONS_EXAMPLES
from app.tests.utils.tables import create_table


async def test_create_table(db: Session, faker: Faker) -> None:
    new_table_data = {
        "name": faker.word(),
        "seats": faker.random_int(1, 5),
        "location": faker.random_element(LOCATIONS_EXAMPLES),
    }

    table_in = TableInput(**new_table_data)
    table = await TableRepository(db).create(table_in)
    assert table.name == new_table_data['name']
    assert table.seats == new_table_data['seats']
    assert table.location == new_table_data['location']


async def test_exists_by_id_table(db: Session, table: TableFactory) -> None:
    assert await TableRepository(db).exists_by_id(table.id)


# TODO: need filter
async def test_is_exists_table(db: Session, table: TableFactory) -> None:
    assert await TableRepository(db).is_exists()


async def test_get_all_table(db: Session) -> None:
    tables_num = random.randint(3, 6)
    [await create_table(db) for _ in range(tables_num)]

    tables = await TableRepository(db).get_all()
    assert len(tables) == tables_num


async def test_get_by_id_table(db: Session, table: TableFactory) -> None:
    table_obj = await TableRepository(db).get_by_id(table.id)

    assert table_obj.id == table.id
    assert table_obj.name == table.name
    assert table_obj.seats == table.seats
    assert table_obj.location == table.location


async def test_update_table(db: Session, faker: Faker) -> None:
    table = await create_table(db)

    new_table_data = {
        "name": faker.word(),
        "seats": faker.random_int(6, 10),
        "location": faker.sentence(nb_words=3),
    }
    table_in = TableInput(**new_table_data)

    assert table.name != table_in.name
    assert table.seats != table_in.seats
    assert table.location != table_in.location

    await TableRepository(db).update(table, table_in)

    assert table.name == table_in.name
    assert table.seats == table_in.seats
    assert table.location == table_in.location


async def test_delete_table(db: Session) -> None:
    table = await create_table(db)
    await TableRepository(db).delete(table)

    assert not await TableRepository(db).exists_by_id(table.id)
