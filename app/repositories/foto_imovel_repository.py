from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.foto_imovel_model import FotoImovelModel
from app.repositories.base_repository import BaseRepository

class FotoImovelRepository(BaseRepository[FotoImovelModel]):
    def __init__(self):
        super().__init__(FotoImovelModel)

    def get_by_imovel(self, db: AsyncSession, imovel_id: int):
        stmt = select(FotoImovelModel).where(FotoImovelModel.imovel_id == imovel_id)
        result =  db.execute(stmt)
        return result.scalars().all()