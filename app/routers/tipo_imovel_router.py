from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.services.tipo_imovel_service import TipoImovelService
from app.repositories.tipo_imovel_repository import TipoImovelRepository
from app.schemas.tipo_imovel_schema import TipoImovelBase,TipoImovelRead
from app.core.security import obter_usuario_corrente  # importa a função

router = APIRouter(prefix="/tipoimovel", tags=["tipoimovel"])

def get_cliente_service(db: Session = Depends(get_db)):
    repository = TipoImovelRepository(db)
    service = TipoImovelService(repository)
    return service



@router.get("/", response_model=list[TipoImovelRead])
async def listar_tipoimovel(
    service: TipoImovelService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    return service.listar_cliente()

@router.get("/{tipoimovel_id}", response_model=TipoImovelRead)
async def get_tipoimovel(
    tipoimovel_id: int,
    service: TipoImovelService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    tipoimovel = service.buscar_por_id(tipoimovel_id)
    return tipoimovel
