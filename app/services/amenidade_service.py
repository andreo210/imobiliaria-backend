from app.repositories.cliente_repository import ClienteRepository
from app.schemas.amenidade_schema import AmenidadeCreate,AmenidadeBase,AmenidadeRead
from app.models.amenidade_model import AmenidadeModel

class AmenidadeService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def criar_amenidade(self, amenidade: AmenidadeCreate):
        nova_amenidade = AmenidadeModel(
            nome=amenidade.nome
        )
        return self.repository.create(nova_amenidade)

    def listar_amenidade(self):
        return self.repository.get_all()

    def buscar_por_id(self, id: int):
        return self.repository.get_by_id(id)

    async def deletar(self, id: int):
        return  self.repository.delete(id)