from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self, db: AsyncSession) -> List[ModelType]:
        stmt = select(self.model)
        result = db.execute(stmt)
        return result.scalars().all()

    def create(self, db: AsyncSession, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: AsyncSession, id: int) -> bool:
        obj = self.get(db, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

    def update(self, db: AsyncSession, id: int, data: dict) -> Optional[ModelType]:
        obj = self.get(db, id)
        if not obj:
            return None
        for field, value in data.items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj
