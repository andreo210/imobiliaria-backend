from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioBase, UsuarioCreate,UsuarioResponse
from app.core.security import obter_usuario_corrente,verificar_admin  # importa a funções de segurança

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_usuario_service(db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    return service

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    usuario: UsuarioCreate,
    service: UsuarioService = Depends(get_usuario_service),
    usuario_atual: dict = Depends(verificar_admin)  # Corrigido: sem parênteses
):
    """
    Cria um novo usuário
    Apenas administradores podem criar usuários
    """
    try:
        return service.criar_usuario(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=list[UsuarioResponse])
def listar(service: UsuarioService = Depends(get_usuario_service)):
    return service.listar_usuarios()


@router.get("/{usuarios_id}", response_model=UsuarioResponse)
async def get_cliente(
    usuarios_id: int,
    service: UsuarioService = Depends(get_usuario_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    cliente = service.buscar_por_id(usuarios_id)
    return cliente

@router.put("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar(usuario_id: int, usuario_update: UsuarioBase ,service: UsuarioService = Depends(get_usuario_service)):
    model = service.atualizar(usuario_id, usuario_update)
    if not model:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return model

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(usuario_id: int,service: UsuarioService = Depends(get_usuario_service)):
    usuario = service.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    model = service.deletar(usuario)

    return model
