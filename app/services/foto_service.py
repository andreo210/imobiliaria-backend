from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.foto_imovel_model import FotoImovelModel
from app.schemas.foto_imovel_schema import (
    FotoImovelCreate,
    FotoImovelUpdate
)
from app.repositories.foto_imovel_repository import FotoImovelRepository

foto_repo = FotoImovelRepository()


class FotoService:

    @staticmethod
    async def listar_por_imovel(db: AsyncSession, imovel_id: int) -> List[FotoImovelModel]:
        result = await foto_repo.obter_id_imovel(db, imovel_id)
        return result

    @staticmethod
    async def obter(db: AsyncSession, id: int) -> Optional[FotoImovelModel]:
        return  await foto_repo.obter_id(db, id)

    @staticmethod
    async def criar(db: AsyncSession, data: FotoImovelCreate) -> FotoImovelModel:
        foto = FotoImovelModel(
            imovel_id=data.imovel_id,
            url=data.url
        )
        return await foto_repo.criar(db, foto)

    @staticmethod
    async def atualizar(db: AsyncSession, id: int, data: FotoImovelUpdate) -> Optional[FotoImovelModel]:
        update_dict = data.model_dump(exclude_unset=True)
        return await foto_repo.atualizar(db, id, update_dict)

    @staticmethod
    async def excluir(db: AsyncSession, id: int) -> bool:
        return await foto_repo.deletar(db, id)
