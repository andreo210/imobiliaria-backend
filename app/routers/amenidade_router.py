from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.amenidade_service import  AmenidadeService
from app.schemas.amenidade_schema import AmenidadeCreate,AmenidadeRead

service = AmenidadeService()
router = APIRouter(prefix="/amenidades", tags=["Amenidades"])


@router.post("/", response_model=AmenidadeRead)
async def criar_amenidade(amenidade: AmenidadeCreate,db: AsyncSession = Depends(get_db) ):
    try:
        return await service.criar_amenidade(db,amenidade)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{amenidade_id}", response_model=AmenidadeRead)
async def get_amenidade(amenidade_id: int,db: AsyncSession = Depends(get_db)):
    amenidade = await service.buscar_por_id(db,amenidade_id)
    if not amenidade:
        raise HTTPException(status_code=404, detail="Amenidade não encontrada")
    return amenidade

@router.get("/", response_model=list[AmenidadeRead])
async def listar_amenidade(db: AsyncSession = Depends(get_db)):
    return await service.listar_amenidade(db)

@router.delete("/{amenidade_id}", status_code=204)
async def del_amenidade(amenidade_id: int,db: AsyncSession = Depends(get_db)):
    await service.deletar(db,amenidade_id)

