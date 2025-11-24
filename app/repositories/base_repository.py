from typing import Generic, TypeVar, Type, List, Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def obter_email(self, db: AsyncSession, email: EmailStr) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def obter_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def obter_todos(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def criar(self, db: AsyncSession, obj: ModelType) -> ModelType:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def deletar(self, db: AsyncSession, id: int) -> bool:
        obj = await self.obter_id(db, id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True

    async def atualizar(self, db: AsyncSession, id: int, data: dict) -> Optional[ModelType]:
        obj = await self.obter_id(db, id)
        if not obj:
            return None

        for field, value in data.items():
            setattr(obj, field, value)

        await db.commit()
        await db.refresh(obj)
        return obj
