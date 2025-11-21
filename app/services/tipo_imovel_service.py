from app.repositories.tipo_imovel_repository import TipoImovelRepository


class TipoImovelService:
    def __init__(self, repository: TipoImovelRepository):
        self.repository = repository

    def listar_cliente(self):
        return self.repository.get_all()

    def buscar_por_id(self, id: int):
        return self.repository.get_by_id(id)

