from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    papel: str
    senha : str

class UsuarioRead(BaseModel):
    nome: str
    email: EmailStr
    papel: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioRead):
    id: int
    criado_em: datetime

    model_config = {
        "from_attributes": True
    }