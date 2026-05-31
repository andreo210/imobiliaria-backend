from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.amenidade_service import AmenidadeService
from app.repositories.amenidade_repository import AmenidadeRepository
from app.schemas.amenidade_schema import AmenidadeCreate, AmenidadeRead

router = APIRouter(prefix="/amenidades", tags=["Amenidades"])


def get_amenidade_service():
    repository = AmenidadeRepository()
    return AmenidadeService(repository)


@router.post("/", response_model=AmenidadeRead)
async def criar_amenidade(
    amenidade: AmenidadeCreate,
    db: AsyncSession = Depends(get_db),
    service: AmenidadeService = Depends(get_amenidade_service)
):
    try:
        return await service.criar_amenidade(db, amenidade)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{amenidade_id}", response_model=AmenidadeRead)
async def get_amenidade(
    amenidade_id: int,
    db: AsyncSession = Depends(get_db),
    service: AmenidadeService = Depends(get_amenidade_service)
):
    amenidade = await service.buscar_por_id(db, amenidade_id)
    if not amenidade:
        raise HTTPException(status_code=404, detail="Amenidade não encontrada")
    return amenidade


@router.get("/", response_model=list[AmenidadeRead])
async def listar_amenidade(
    db: AsyncSession = Depends(get_db),
    service: AmenidadeService = Depends(get_amenidade_service)
):
    return await service.listar_amenidade(db)


@router.delete("/{amenidade_id}", status_code=204)
async def del_amenidade(
    amenidade_id: int,
    db: AsyncSession = Depends(get_db),
    service: AmenidadeService = Depends(get_amenidade_service)
):
    ok = await service.deletar(db, amenidade_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Amenidade não encontrada")

