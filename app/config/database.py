
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from .settings import settings

engine = create_engine(settings.POSTGRES_CONNECTION_STRING)

Base = declarative_base()


def init_db(session: Session) -> None:
    Base.metadata.create_all(engine)
