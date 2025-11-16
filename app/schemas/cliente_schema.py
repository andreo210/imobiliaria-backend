from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int
    criado_em: datetime

    model_config = {
        "from_attributes": True
    }