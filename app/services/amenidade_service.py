from app.repositories.base_repository import BaseRepository
from app.schemas.amenidade_schema import AmenidadeCreate
from app.models.amenidade_model import AmenidadeModel
from sqlalchemy.ext.asyncio import AsyncSession


class AmenidadeService:

    @staticmethod
    async def criar_amenidade(db: AsyncSession, amenidade: AmenidadeCreate):
        repo = BaseRepository(AmenidadeModel)
        nova_amenidade = AmenidadeModel(nome=amenidade.nome)
        return await repo.criar(db, nova_amenidade)

    @staticmethod
    async def listar_amenidade(db: AsyncSession):
        repo = BaseRepository(AmenidadeModel)
        return await repo.obter_todos(db)

    @staticmethod
    async def buscar_por_id(db: AsyncSession, id: int):
        repo = BaseRepository(AmenidadeModel)
        return await repo.obter_id(db, id)

    @staticmethod
    async def deletar(db: AsyncSession, id: int):
        repo = BaseRepository(AmenidadeModel)
        return await repo.deletar(db, id)
