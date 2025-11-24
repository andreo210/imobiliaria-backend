from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.tipo_imovel_service import TipoImovelService
from app.repositories.tipo_imovel_repository import TipoImovelRepository
from app.schemas.tipo_imovel_schema import TipoImovelRead
from app.core.security import obter_usuario_corrente  # importa a função

router = APIRouter(prefix="/tipoimovel", tags=["tipoimovel"])

def get_cliente_service():
    repository = TipoImovelRepository()
    service = TipoImovelService(repository)
    return service



@router.get("/", response_model=list[TipoImovelRead])
async def listar_tipoimovel(service: TipoImovelService = Depends(get_cliente_service), db: AsyncSession = Depends(get_db)):
    return await service.listar_cliente(db)

@router.get("/{tipoimovel_id}", response_model=TipoImovelRead)
async def get_tipoimovel(
    tipoimovel_id: int,
    db: AsyncSession = Depends(get_db),
    service: TipoImovelService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    tipoimovel = await service.buscar_por_id(tipoimovel_id,db)
    return tipoimovel
