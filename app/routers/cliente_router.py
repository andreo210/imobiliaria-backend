from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.services.cliente_service import ClienteService
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate, ClienteRead,ClienteBase
from app.core.security import obter_usuario_corrente  # importa a função

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_cliente_service(db: Session = Depends(get_db)):
    repository = ClienteRepository(db)
    service = ClienteService(repository)
    return service

@router.post("/", response_model=ClienteRead)
async def criar_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service)
     # protege rota
):
    try:
        return service.criar_cliente(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_cliente(cliente_id: int, cliente_update: ClienteBase ,service: ClienteService = Depends(get_cliente_service)):
    model = service.atualizar(cliente_id, cliente_update)
    if not model:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return model

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_cliente(cliente_id: int,service: ClienteService = Depends(get_cliente_service)):
    cliente = service.buscar_por_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    model = service.deletar(cliente)

    return model

@router.get("/", response_model=list[ClienteRead])
async def listar_cliente(
    service: ClienteService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    return service.listar_cliente()

@router.get("/{cliente_id}", response_model=ClienteRead)
async def get_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    cliente = service.buscar_por_id(cliente_id)
    return cliente
