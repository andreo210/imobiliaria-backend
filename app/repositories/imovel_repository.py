from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.imovel_model import ImovelModel
from app.repositories.base_repository import BaseRepository

class ImovelRepository(BaseRepository[ImovelModel]):
    def __init__(self):
        super().__init__(ImovelModel)

    def get_full(self, db: AsyncSession, id: int):
        stmt = (
            select(ImovelModel)
            .where(ImovelModel.id == id)
            .options(
                selectinload(ImovelModel.fotos),
                selectinload(ImovelModel.amenidades),
                selectinload(ImovelModel.tipo),
            )
        )

        result = db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all_full(self, db: AsyncSession):
        stmt = (
            select(ImovelModel)
            .options(
                selectinload(ImovelModel.fotos),
                selectinload(ImovelModel.amenidades),
                selectinload(ImovelModel.tipo),
            )
        )
        result = db.execute(stmt)
        return result.scalars().all()
