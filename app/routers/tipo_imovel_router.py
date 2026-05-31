from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.tipo_imovel_service import TipoImovelService
from app.repositories.tipo_imovel_repository import TipoImovelRepository
from app.schemas.tipo_imovel_schema import TipoImovelRead

router = APIRouter(prefix="/tipoimovel", tags=["tipoimovel"])

def get_tipo_imovel_service():
    repository = TipoImovelRepository()
    return TipoImovelService(repository)


@router.get("/", response_model=list[TipoImovelRead])
async def listar_tipoimovel(
    service: TipoImovelService = Depends(get_tipo_imovel_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.listar_tipoimovel(db)


@router.get("/{tipoimovel_id}", response_model=TipoImovelRead)
async def get_tipoimovel(
    tipoimovel_id: int,
    db: AsyncSession = Depends(get_db),
    service: TipoImovelService = Depends(get_tipo_imovel_service)
):
    tipoimovel = await service.buscar_por_id(tipoimovel_id, db)
    return tipoimovel
