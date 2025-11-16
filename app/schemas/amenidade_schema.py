from pydantic import BaseModel, EmailStr
from datetime import datetime

class AmenidadeBase(BaseModel):
    nome: str

class AmenidadeCreate(AmenidadeBase):
    pass

class AmenidadeRead(AmenidadeBase):
    id: int

    model_config = {
        "from_attributes": True
    }