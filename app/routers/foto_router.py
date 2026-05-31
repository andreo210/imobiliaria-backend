from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.foto_imovel_schema import (
    FotoImovelCreate,
    FotoImovelUpdate,
    FotoImovelResponse
)
from app.services.foto_service import FotoService
from app.repositories.foto_imovel_repository import FotoImovelRepository

router = APIRouter(prefix="/fotos", tags=["Fotos"])


def get_foto_service():
    repository = FotoImovelRepository()
    return FotoService(repository)


@router.get("/imovel/{imovel_id}", response_model=list[FotoImovelResponse])
async def listar_fotos(
    imovel_id: int,
    db: AsyncSession = Depends(get_db),
    service: FotoService = Depends(get_foto_service)
):
    return await service.listar_por_imovel(db, imovel_id)


@router.get("/{id}", response_model=FotoImovelResponse)
async def obter_foto(
    id: int,
    db: AsyncSession = Depends(get_db),
    service: FotoService = Depends(get_foto_service)
):
    foto = await service.obter(db, id)
    if not foto:
        raise HTTPException(404, "Foto não encontrada")
    return foto


@router.post("/", response_model=FotoImovelResponse, status_code=201)
async def criar_foto(
    payload: FotoImovelCreate,
    db: AsyncSession = Depends(get_db),
    service: FotoService = Depends(get_foto_service)
):
    return await service.criar(db, payload)


@router.put("/{id}", response_model=FotoImovelResponse)
async def atualizar_foto(
    id: int,
    payload: FotoImovelUpdate,
    db: AsyncSession = Depends(get_db),
    service: FotoService = Depends(get_foto_service)
):
    foto = await service.atualizar(db, id, payload)
    if not foto:
        raise HTTPException(404, "Foto não encontrada")
    return foto


@router.delete("/{id}", status_code=204)
async def excluir_foto(
    id: int,
    db: AsyncSession = Depends(get_db),
    service: FotoService = Depends(get_foto_service)
):
    ok = await service.excluir(db, id)
    if not ok:
        raise HTTPException(404, "Foto não encontrada")
