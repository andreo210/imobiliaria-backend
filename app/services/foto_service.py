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
    def listar_por_imovel(db: AsyncSession, imovel_id: int) -> List[FotoImovelModel]:
        return foto_repo.get_by_imovel(db, imovel_id)

    @staticmethod
    def obter(db: AsyncSession, id: int) -> Optional[FotoImovelModel]:
        return  foto_repo.get(db, id)

    @staticmethod
    def criar(db: AsyncSession, data: FotoImovelCreate) -> FotoImovelModel:
        foto = FotoImovelModel(
            imovel_id=data.imovel_id,
            url=data.url
        )
        return foto_repo.create(db, foto)

    @staticmethod
    def atualizar(db: AsyncSession, id: int, data: FotoImovelUpdate) -> Optional[FotoImovelModel]:
        update_dict = data.model_dump(exclude_unset=True)
        return foto_repo.update(db, id, update_dict)

    @staticmethod
    def excluir(db: AsyncSession, id: int) -> bool:
        return foto_repo.delete(db, id)
