from typing import Optional
from pydantic import BaseModel, Field

class TipoImovelBase(BaseModel):
    nome: str

class TipoImovelRead(TipoImovelBase):
    id: int

class TipoImovelUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)

    model_config = {
        "from_attributes": True
    }