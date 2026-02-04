from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: Any) -> Optional[ModelType]:
        return await self.db.get(self.model, id)

    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        query = select(self.model).where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, obj_in: Any, autocommit: bool = False) -> ModelType:
        db_obj = self.model(**obj_in.dict()) if hasattr(obj_in, 'dict') else self.model(**obj_in)
        self.db.add(db_obj)
        if autocommit:
            await self.db.commit()
            await self.db.refresh(db_obj)
        return db_obj
