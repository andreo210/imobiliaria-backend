from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate,UsuarioBase,UsuarioResponse
from app.models.usuario_model import Usuario
from app.utils.hashing import codificar_senha,decodificar_senha

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def criar_usuario(self, usuario_create: UsuarioCreate):
        if self.repository.get_by_email(usuario_create.email):
            raise ValueError("Email já cadastrado")
        novo_usuario = Usuario(
            nome=usuario_create.nome,
            email=usuario_create.email,
            senha=codificar_senha(usuario_create.senha),
            papel=usuario_create.papel
        )
        return self.repository.create(novo_usuario)


    def listar_usuarios(self):

        return self.repository.get_all()

    def buscar_por_id(self, id: int):
        return self.repository.get_by_id(id)

    def deletar(self, model: Usuario):
        return self.repository.delete(model)

    def atualizar(self, id: int, usuario_update: UsuarioBase):
        usuario_update.nome = usuario_update.nome.upper()
        usuario_update.senha = codificar_senha(usuario_update.senha)
        return self.repository.update(id, usuario_update)

    def autenticar(self, email: str, senha: str):
        usuario = self.repository.get_by_email(email)
        if not usuario or not decodificar_senha(senha, usuario.senha):
            return None
        return usuario
