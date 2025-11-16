from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioBase, UsuarioCreate,UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_usuario_service(db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    return service

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return service.criar_usuario(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    return service.listar_usuarios()
