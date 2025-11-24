from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.cliente_service import ClienteService
from app.schemas.cliente_schema import ClienteCreate, ClienteRead,ClienteBase
from app.core.security import obter_usuario_corrente  # importa a função

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteRead)
async def criar_cliente(cliente: ClienteCreate, db: AsyncSession = Depends(get_db)):
    service = ClienteService()
    try:
        return await service.criar_cliente(db,cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_cliente(cliente_id: int, cliente_update: ClienteBase ,db: AsyncSession = Depends(get_db)):
    service = ClienteService()
    model = await service.atualizar(db,cliente_id, cliente_update)
    if not model:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return model

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_cliente(cliente_id: int,db: AsyncSession = Depends(get_db)):
    service = ClienteService()
    cliente = await service.buscar_por_id(db,cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    model = await service.deletar(db,cliente)

    return model

@router.get("/", response_model=list[ClienteRead])
async def listar_cliente(db: AsyncSession = Depends(get_db)):
    service = ClienteService()
    return await service.listar_cliente(db)

@router.get("/{cliente_id}", response_model=ClienteRead)
async def get_cliente(
    cliente_id: int,
    db: AsyncSession = Depends(get_db)
        # protege rota current_user: dict = Depends(get_current_user)
):
    service = ClienteService()
    cliente = await service.buscar_por_id(db,cliente_id)
    return cliente
