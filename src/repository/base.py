from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, DeclarativeBase


class BaseRepository:

    def __init__(self, session: Session, model: DeclarativeBase = None):
        self.session = session
        self.model = model
        self.filter = None

    @property
    def base_query(self):
        query = select([self.model])

        if self.filter:
            query = self.filter(query)
        return query

    async def create(self, data: Any) -> dict:
        db_object = self.model(**data.model_dump())
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        return db_object.__dict__

    async def exists_by_id(self, _id: Any) -> bool:
        return self.session.query(self.model).filter(self.model.pk == _id).first() is not None

    async def is_exists(self) -> bool:
        result = await self.session.scalar(self.base_query)
        return bool(result)

    # TODO: добавить await
    async def get_all(self) -> List[dict]:
        result = self.session.execute(self.base_query)
        # return result.all()
        return [
            obj.__dict__
            for obj in result
        ]

    async def get_by_id(self, _id: Any) -> Optional[dict]:
        obj = self.session.query(self.model).filter(self.model.pk == _id).first()
        if obj:
            return obj.__dict__
        return None

    async def update(self, obj: DeclarativeBase, data: Any) -> dict:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj.__dict__

    async def delete(self, obj: DeclarativeBase) -> bool:
        self.session.delete(obj)
        self.session.commit()
        return True
