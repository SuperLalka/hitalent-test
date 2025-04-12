from faker import Faker
from sqlalchemy.orm import Session

from app.models import Table
from app.repository.table import TableRepository
from app.schemas.table import TableInput
from app.tests.fixtures import LOCATIONS_EXAMPLES

fake = Faker()


async def create_table(
        db: Session,
        name: str = None,
        seats: int = None,
        location: str = None
) -> Table:
    return await TableRepository(db).create(
        TableInput(
            name=name or fake.name(),
            seats=seats or fake.random_int(1, 5),
            location=location or fake.random_element(LOCATIONS_EXAMPLES),
        )
    )
