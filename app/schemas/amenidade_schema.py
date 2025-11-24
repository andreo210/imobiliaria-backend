from typing import List, Optional
from pydantic import BaseModel, Field

class AmenidadeBase(BaseModel):
    nome: str

class AmenidadeCreate(AmenidadeBase):
    pass

class AmenidadeRead(AmenidadeBase):
    id: int

class AmenidadeUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)

    model_config = {
        "from_attributes": True
    }