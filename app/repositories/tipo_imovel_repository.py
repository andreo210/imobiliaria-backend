from app.models.tipo_imovel_model import TipoImovelModel
from app.repositories.base_repository import BaseRepository

class TipoImovelRepository(BaseRepository[TipoImovelModel]):
    def __init__(self):
        super().__init__(TipoImovelModel)





