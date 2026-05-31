from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.foto_imovel_model import FotoImovelModel
from app.schemas.foto_imovel_schema import (
    FotoImovelCreate,
    FotoImovelUpdate
)
from app.repositories.foto_imovel_repository import FotoImovelRepository


class FotoService:
    def __init__(self, repository: FotoImovelRepository):
        self.repository = repository

    async def listar_por_imovel(self, db: AsyncSession, imovel_id: int) -> List[FotoImovelModel]:
        return await self.repository.obter_id_imovel(db, imovel_id)

    async def obter(self, db: AsyncSession, id: int) -> Optional[FotoImovelModel]:
        return await self.repository.obter_id(db, id)

    async def criar(self, db: AsyncSession, data: FotoImovelCreate) -> FotoImovelModel:
        foto = FotoImovelModel(
            imovel_id=data.imovel_id,
            url=data.url
        )
        return await self.repository.criar(db, foto)

    async def atualizar(self, db: AsyncSession, id: int, data: FotoImovelUpdate) -> Optional[FotoImovelModel]:
        update_dict = data.model_dump(exclude_unset=True)
        return await self.repository.atualizar(db, id, update_dict)

    async def excluir(self, db: AsyncSession, id: int) -> bool:
        return await self.repository.deletar(db, id)
