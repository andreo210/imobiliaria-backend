from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.imovel_schema import (
    ImovelCreate,
    ImovelUpdate,
    ImovelResponse
)
from app.services.imovel_service import ImovelService

router = APIRouter(prefix="/imoveis", tags=["Imóveis"])


@router.get("/", response_model=list[ImovelResponse])
def listar_imoveis(db: AsyncSession = Depends(get_db)):
    return  ImovelService.listar(db)


@router.get("/{id}", response_model=ImovelResponse)
def obter_imovel(id: int, db: AsyncSession = Depends(get_db)):
    imovel = ImovelService.obter(db, id)
    if not imovel:
        raise HTTPException(404, "Imóvel não encontrado")
    return imovel


@router.post("/", response_model=ImovelResponse, status_code=201)
def criar_imovel(payload: ImovelCreate, db: AsyncSession = Depends(get_db)):
    return  ImovelService.criar(db, payload)


@router.put("/{id}", response_model=ImovelResponse)
def atualizar_imovel(id: int, payload: ImovelUpdate, db: AsyncSession = Depends(get_db)):
    imovel =  ImovelService.atualizar(db, id, payload)
    if not imovel:
        raise HTTPException(404, "Imóvel não encontrado")
    return imovel


@router.delete("/{id}", status_code=204)
def excluir_imovel(id: int, db: AsyncSession = Depends(get_db)):
    ok = ImovelService.excluir(db, id)
    if not ok:
        raise HTTPException(404, "Imóvel não encontrado")
    return
