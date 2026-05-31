from app.repositories.amenidade_repository import AmenidadeRepository
from app.schemas.amenidade_schema import AmenidadeCreate
from app.models.amenidade_model import AmenidadeModel
from sqlalchemy.ext.asyncio import AsyncSession


class AmenidadeService:
    def __init__(self, repository: AmenidadeRepository):
        self.repository = repository

    async def criar_amenidade(self, db: AsyncSession, amenidade: AmenidadeCreate):
        nova_amenidade = AmenidadeModel(nome=amenidade.nome)
        return await self.repository.criar(db, nova_amenidade)

    async def listar_amenidade(self, db: AsyncSession):
        return await self.repository.obter_todos(db)

    async def buscar_por_id(self, db: AsyncSession, id: int):
        return await self.repository.obter_id(db, id)

    async def deletar(self, db: AsyncSession, id: int):
        return await self.repository.deletar(db, id)
