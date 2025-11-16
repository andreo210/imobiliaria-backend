from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate,ClienteBase,ClienteRead
from app.models.cliente_model import ClienteModel

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def criar_cliente(self, cliente_create: ClienteCreate):
        if self.repository.get_by_email(cliente_create.email):
            raise ValueError("Email já cadastrado")
        novo_cliente = ClienteModel(
            nome=cliente_create.nome,
            email=cliente_create.email,
            telefone=cliente_create.telefone
        )
        return self.repository.create(novo_cliente)

    def listar_cliente(self):
        return self.repository.get_all()

    def buscar_por_id(self, id: int):
        return self.repository.get_by_id(id)
