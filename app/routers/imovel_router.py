from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.imovel_schema import (
    ImovelCreate,
    ImovelUpdate,
    ImovelResponse
)
from app.services.imovel_service import ImovelService
from app.repositories.imovel_repository import ImovelRepository

router = APIRouter(prefix="/imoveis", tags=["Imóveis"])


def get_imovel_service():
    repository = ImovelRepository()
    return ImovelService(repository)


@router.get("/", response_model=list[ImovelResponse])
async def listar_imoveis(
    db: AsyncSession = Depends(get_db),
    service: ImovelService = Depends(get_imovel_service)
):
    return await service.listar(db)


@router.get("/{id}", response_model=ImovelResponse)
async def obter_imovel(
    id: int,
    db: AsyncSession = Depends(get_db),
    service: ImovelService = Depends(get_imovel_service)
):
    imovel = await service.obter(db, id)
    if not imovel:
        raise HTTPException(404, "Imóvel não encontrado")
    return imovel


@router.post("/", response_model=ImovelResponse, status_code=201)
async def criar_imovel(
    payload: ImovelCreate,
    db: AsyncSession = Depends(get_db),
    service: ImovelService = Depends(get_imovel_service)
):
    return await service.criar(db, payload)


@router.put("/{id}", response_model=ImovelResponse)
async def atualizar_imovel(
    id: int,
    payload: ImovelUpdate,
    db: AsyncSession = Depends(get_db),
    service: ImovelService = Depends(get_imovel_service)
):
    imovel = await service.atualizar(db, id, payload)
    if not imovel:
        raise HTTPException(404, "Imóvel não encontrado")
    return imovel


@router.delete("/{id}", status_code=204)
async def excluir_imovel(
    id: int,
    db: AsyncSession = Depends(get_db),
    service: ImovelService = Depends(get_imovel_service)
):
    ok = await service.excluir(db, id)
    if not ok:
        raise HTTPException(404, "Imóvel não encontrado")
