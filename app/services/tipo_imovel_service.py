from app.repositories.tipo_imovel_repository import TipoImovelRepository
from sqlalchemy.ext.asyncio import AsyncSession

class TipoImovelService:
    def __init__(self, repository: TipoImovelRepository):
        self.repository = repository

    async def listar_cliente(self, db: AsyncSession):
        return await self.repository.obter_todos(db)

    async def buscar_por_id(self, id: int,db: AsyncSession ):
        return await self.repository.obter_id(db,id)

