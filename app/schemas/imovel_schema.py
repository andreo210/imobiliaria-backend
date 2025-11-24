from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.amenidade_schema import AmenidadeRead
from app.schemas.foto_imovel_schema import FotoImovelCreate,FotoImovelResponse
from app.schemas.tipo_imovel_schema import TipoImovelUpdate,TipoImovelRead,TipoImovelBase

class ImovelBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    preco: float
    status: str   # ou enum se quiser
    tipo_id: Optional[int] = None
    usuario_id: Optional[int] = None

class ImovelCreate(ImovelBase):
    amenidades_ids: Optional[List[int]] = []
    fotos: Optional[List[FotoImovelCreate]] = []

class ImovelUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    status: Optional[str] = None
    tipo_id: Optional[int] = None
    usuario_id: Optional[int] = None
    amenidades_ids: Optional[List[int]] = None

class ImovelResponse(ImovelBase):
    id: int
    criado_em: datetime
    tipo: Optional[TipoImovelRead] = None
    fotos: List[FotoImovelResponse] = []
    amenidades: List[AmenidadeRead] = []

    class Config:
        from_attributes = True