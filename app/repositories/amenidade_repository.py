from app.models.amenidade_model import AmenidadeModel
from app.repositories.base_repository import BaseRepository

class AmenidadeRepository(BaseRepository[AmenidadeModel]):
    def __init__(self):
        super().__init__(AmenidadeModel)


