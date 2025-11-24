from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate,UsuarioBase
from app.models.usuario_model import Usuario
from app.utils.hashing import codificar_senha,decodificar_senha
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    async def criar_usuario(self, db: AsyncSession, usuario_create: UsuarioCreate):
        # verificar se email já existe
        existente = await self.repository.obter_email(db, usuario_create.email)
        if existente:
            raise ValueError("Email já cadastrado")

        novo_usuario = Usuario(
            nome=usuario_create.nome,
            email=usuario_create.email,
            senha=codificar_senha(usuario_create.senha),
            papel=usuario_create.papel
        )
        return await self.repository.criar(db, novo_usuario)


    async def listar_usuarios(self, db: AsyncSession):
        return await self.repository.obter_todos(db)

    async def buscar_por_id(self, db: AsyncSession, id: int):
        return await self.repository.obter_id(db, id)

    async def deletar(self, db: AsyncSession, model: Usuario):
        return await self.repository.deletar(db, model.id)

    async def atualizar(self, db: AsyncSession, id: int, usuario_update: UsuarioBase):
        update_dict = usuario_update.model_dump(exclude_unset=True)
        update_dict["senha"] = codificar_senha(usuario_update.senha)
        return await self.repository.atualizar(db, id, update_dict)

    async def autenticar(self, db: AsyncSession, email: EmailStr, senha: str):
        usuario = await self.repository.obter_email(db, email)
        if not usuario or not decodificar_senha(senha, usuario.senha):
            return None
        return usuario
