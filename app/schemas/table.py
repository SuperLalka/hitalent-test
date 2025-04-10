from typing import Optional

from pydantic import BaseModel, field_validator


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None


class TableInput(TableBase):

    @field_validator('seats', mode='before')
    @classmethod
    def validate_seats(cls, value: int):
        if value < 0:
            raise ValueError('Seats must be a positive number.')
        return value


class TableOutput(TableBase):
    id: str
