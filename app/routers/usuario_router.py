from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioBase, UsuarioCreate, UsuarioResponse
from app.core.security import verificar_admin  # funções de segurança

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Dependência para injetar o service
def get_usuario_service(db: AsyncSession = Depends(get_db)):
    repository = UsuarioRepository()
    service = UsuarioService(repository)
    return service


@router.post("/", response_model=UsuarioResponse)
async def criar_usuario(
    usuario: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service),
    usuario_atual: dict = Depends(verificar_admin)  # apenas admin pode criar
):
    """
    Cria um novo usuário.
    Apenas administradores podem criar usuários.
    """
    try:
        return await service.criar_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/", response_model=list[UsuarioResponse])
async def listar(
    db: AsyncSession = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service)
):
    return await service.listar_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = await service.buscar_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar(
    usuario_id: int,
    usuario_update: UsuarioBase,
    db: AsyncSession = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service)
):
    model = await service.atualizar(db, usuario_id, usuario_update)
    if not model:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return model


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service)
):
    usuario = await service.buscar_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await service.deletar(db, usuario)
