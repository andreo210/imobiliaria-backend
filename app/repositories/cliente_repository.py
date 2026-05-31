from app.models.cliente_model import ClienteModel
from app.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[ClienteModel]):
    def __init__(self):
        super().__init__(ClienteModel)


