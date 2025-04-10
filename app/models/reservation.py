import datetime
import uuid

from sqlalchemy import (
    func,
    inspect,
    BIGINT,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UUID
)
from sqlalchemy.orm import relationship

from app.config.database import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String, nullable=False)
    reservation_time = Column(DateTime, default=func.now())
    duration_minutes = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    table_id = Column(
        BIGINT,
        ForeignKey("table.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    table = relationship("Table", back_populates="reservations")

    @property
    def reservation_time_end(self) -> datetime.datetime:
        return self.reservation_time + datetime.timedelta(minutes=self.duration_minutes)


reservation = inspect(Reservation).local_table
