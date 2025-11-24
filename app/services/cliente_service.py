from app.repositories.base_repository import BaseRepository
from app.schemas.cliente_schema import ClienteCreate,ClienteBase,ClienteRead
from app.models.cliente_model import ClienteModel
from sqlalchemy.ext.asyncio import AsyncSession

class ClienteService:

    @staticmethod
    async def criar_cliente(db:AsyncSession, cliente_create: ClienteCreate):
        repo = BaseRepository(ClienteModel)
        email = await repo.obter_email(db,cliente_create.email)
        if email:
            raise ValueError("Email já cadastrado")
        novo_cliente = ClienteModel(
            nome=cliente_create.nome,
            email=cliente_create.email,
            telefone=cliente_create.telefone,
            observacao=cliente_create.observacao
        )
        return await repo.criar(db,novo_cliente)

    @staticmethod
    async def listar_cliente(db: AsyncSession):
        repo = BaseRepository(ClienteModel)
        return await repo.obter_todos(db)

    @staticmethod
    async def buscar_por_id(db: AsyncSession, id: int):
        repo = BaseRepository(ClienteModel)
        return await repo.obter_id(db,id)

    @staticmethod
    async def deletar(db: AsyncSession, model: ClienteModel):
        repo = BaseRepository(ClienteModel)
        return await repo.deletar(db,model.id)

    @staticmethod
    async def atualizar(db: AsyncSession, id: int, data: ClienteBase):
        repo = BaseRepository(ClienteModel)
        update_dict = data.model_dump(exclude_unset=True)
        return await repo.atualizar(db,id,update_dict)