from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate, ClienteBase
from app.models.cliente_model import ClienteModel
from sqlalchemy.ext.asyncio import AsyncSession

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    async def criar_cliente(self, db: AsyncSession, cliente_create: ClienteCreate):
        email = await self.repository.obter_email(db, cliente_create.email)
        if email:
            raise ValueError("Email já cadastrado")
        novo_cliente = ClienteModel(
            nome=cliente_create.nome,
            email=cliente_create.email,
            telefone=cliente_create.telefone,
            observacao=cliente_create.observacao
        )
        return await self.repository.criar(db, novo_cliente)

    async def listar_cliente(self, db: AsyncSession):
        return await self.repository.obter_todos(db)

    async def buscar_por_id(self, db: AsyncSession, id: int):
        return await self.repository.obter_id(db, id)

    async def deletar(self, db: AsyncSession, model: ClienteModel):
        return await self.repository.deletar(db, model.id)

    async def atualizar(self, db: AsyncSession, id: int, data: ClienteBase):
        update_dict = data.model_dump(exclude_unset=True)
        return await self.repository.atualizar(db, id, update_dict)