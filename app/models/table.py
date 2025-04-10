
from sqlalchemy import (
    func,
    inspect,
    BIGINT,
    Column,
    DateTime,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(BIGINT, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    seats = Column(Integer, nullable=False, default=1)
    location = Column(String(50))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    reservations = relationship("Reservation", back_populates="table")


table = inspect(Table).local_table
