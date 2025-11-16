from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.amenidade_service import  AmenidadeService
from app.repositories.amenidade_repository import AmenidadeRepository
from app.schemas.amenidade_schema import AmenidadeCreate,AmenidadeBase,AmenidadeRead

router = APIRouter(prefix="/amenidades", tags=["Amenidades"])

def get_amenidade_service(db: Session = Depends(get_db)):
    repository = AmenidadeRepository(db)
    service = AmenidadeService(repository)
    return service

@router.post("/", response_model=AmenidadeRead)
async def criar_amenidade(amenidade: AmenidadeCreate, service: AmenidadeService = Depends(get_amenidade_service)):
    try:
        return service.criar_amenidade(amenidade)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{amenidade_id}", response_model=AmenidadeRead)
async def get_amenidade(amenidade_id: int,service: AmenidadeService = Depends(get_amenidade_service)):
    amenidade = service.buscar_por_id(amenidade_id)
    if not amenidade:
        raise HTTPException(status_code=404, detail="Amenidade não encontrada")
    return amenidade

@router.get("/", response_model=list[AmenidadeRead])
async def listar_amenidade(service: AmenidadeService = Depends(get_amenidade_service)):
    return service.listar_amenidade()

@router.delete("/{amenidade_id}", status_code=204)
async def del_amenidade(amenidade_id: int,service: AmenidadeService = Depends(get_amenidade_service)):
    await service.deletar(amenidade_id)

