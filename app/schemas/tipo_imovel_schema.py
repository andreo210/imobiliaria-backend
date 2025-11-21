from pydantic import BaseModel


class TipoImovelBase(BaseModel):
    nome: str

class TipoImovelRead(TipoImovelBase):
    id: int


    model_config = {
        "from_attributes": True
    }