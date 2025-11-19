from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cliente_service import ClienteService
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import ClienteCreate, ClienteRead
from app.core.security import get_current_user  # importa a função

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

@router.get("/{cliente_id}", response_model=ClienteRead)
async def get_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    cliente = service.buscar_por_id(cliente_id)
    return cliente

@router.get("/", response_model=list[ClienteRead])
async def listar_cliente(
    service: ClienteService = Depends(get_cliente_service)
        # protege rota current_user: dict = Depends(get_current_user)
):
    return service.listar_cliente()
