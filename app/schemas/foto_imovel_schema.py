from datetime import datetime
from typing import  Optional
from pydantic import BaseModel, Field


class FotoImovelBase(BaseModel):
    url: str = Field(..., max_length=255)

class FotoImovelCreate(FotoImovelBase):
    imovel_id: int

class FotoImovelUpdate(BaseModel):
    url: Optional[str] = Field(None, max_length=255)

class FotoImovelResponse(FotoImovelBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True