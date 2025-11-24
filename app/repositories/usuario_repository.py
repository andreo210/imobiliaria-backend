from app.repositories.base_repository import BaseRepository
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioBase
from sqlalchemy.ext.asyncio import AsyncSession

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)
