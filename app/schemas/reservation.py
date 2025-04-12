import datetime
from typing import Optional

from pydantic import field_validator, BaseModel, UUID4

from app.config.settings import settings


class ReservationBase(BaseModel):
    customer_name: str
    reservation_time: datetime.datetime
    duration_minutes: int

    table_id: int


class ReservationInput(ReservationBase):

    @field_validator('duration_minutes', mode='before')
    @classmethod
    def validate_duration(cls, value: int):
        if value < 0:
            raise ValueError('Duration must be a positive number.')
        return value

    @field_validator('reservation_time', mode='before')
    @classmethod
    def validate_reservation_time(cls, value: str):
        if datetime.datetime.strptime(value, settings.DATETIME_PATTERN) < datetime.datetime.now():
            raise ValueError('You cannot specify past time for reservation.')
        return value


class ReservationUpdate(ReservationInput):
    table_id: Optional[int] = None


class ReservationOutput(ReservationBase):
    id: UUID4
