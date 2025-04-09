from typing import Any, List, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repository.base import BaseRepository


class BaseService:

    def __init__(self, session: Session):
        self.repository = BaseRepository(session)

    async def create(self, data: Any) -> Any:
        return await self.repository.create(data)

    async def is_exists(self, _id: Union[str, int]) -> bool:
        return await self.repository.exists_by_id(_id)

    async def get_all(self) -> List[Any]:
        return await self.repository.get_all()

    async def get_by_id(self, _id: Union[str, int]) -> Any:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Object not found")
        return await self.repository.get_by_id(_id)

    async def filter(self, data: Any) -> Any:
        obj = await self.repository.filter(data)
        return await self.repository.filter(obj, data)

    async def update(self, _id: Union[str, int], data: Any) -> Any:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Object not found")

        obj = await self.repository.get_by_id(_id)
        return await self.repository.update(obj, data)

    async def delete(self, _id: Union[str, int]) -> bool:
        if not await self.repository.exists_by_id(_id):
            raise HTTPException(status_code=404, detail="Object not found")

        obj = await self.repository.get_by_id(_id)
        await self.repository.delete(obj)
        return True
