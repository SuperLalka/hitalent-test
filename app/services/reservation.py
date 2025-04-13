from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.filters.reservation import ReservationFilter
from app.repository.reservation import ReservationRepository
from app.services.base import BaseService


class ReservationService(BaseService):

    def __init__(self, session: Session, *args, **kwargs):
        super(ReservationService, self).__init__(session, *args, **kwargs)
        self.repository = ReservationRepository(session, model_filter=kwargs.get('model_filter'))

    async def create(self, data: Any) -> Any:
        self.repository.model_filter = ReservationFilter(
            **{
                'table_id': data.table_id,
                'period': data.reservation_time,
            }
        )

        if await self.repository.is_exists():
            raise HTTPException(status_code=400, detail="The table for the specified time has been reserved.")

        return await self.repository.create(data)
