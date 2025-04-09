import datetime

from pydantic import field_validator, model_validator, BaseModel, UUID4

from src.config.database import get_db
from src.repository.filters.reservation import ReservationFilter
from src.repository.reservation import ReservationRepository


class ReservationBase(BaseModel):
    id: UUID4
    customer_name: str
    reservation_time: datetime.datetime
    duration_minutes: int

    table_id: str


class ReservationInput(ReservationBase):

    @model_validator(mode='before')
    async def validate(self):
        if await ReservationRepository(get_db(), filter=ReservationFilter(
                reservation_time=self.reservation_time,
                reservation_time_end=self.reservation_time + datetime.timedelta(minutes=self.duration_minutes)
        )).is_exists():
            raise ValueError('The table for the specified time has been reserved.')
        return self

    @field_validator('duration_minutes', mode='before')
    @classmethod
    def validate_duration(cls, value: int):
        if value < 0:
            raise ValueError('Duration must be a positive number.')
        return value

    @field_validator('reservation_time', mode='before')
    @classmethod
    def validate_reservation_time(cls, value: datetime.datetime):
        if value < datetime.datetime.now():
            raise ValueError('You cannot specify past time for reservation.')
        return value


class ReservationOutput(ReservationBase):
    pass
