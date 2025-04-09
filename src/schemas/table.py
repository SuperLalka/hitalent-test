from typing import Optional

from pydantic import BaseModel


class TableBase(BaseModel):
    id: str
    name: str
    seats: int
    location: Optional[str] = None


class TableInput(TableBase):
    pass


class TableOutput(TableBase):
    pass
