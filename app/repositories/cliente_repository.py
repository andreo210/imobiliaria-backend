from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
from app.schemas.cliente_schema import ClienteBase

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(ClienteModel).filter(ClienteModel.email == email).first()

    def create(self, cliente: ClienteModel):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get_all(self):
        return self.db.query(ClienteModel).all()

    def get_by_id(self, id: int):
        return self.db.query(ClienteModel).filter(ClienteModel.id == id).first()

    def delete(self, usuario: ClienteModel):
        self.db.delete(usuario)
        self.db.commit()

    def update(self, id: int, data: ClienteBase):
        model = self.get_by_id(id)
        if not model:
            return None
        # Atualiza apenas os campos enviados
        for field, value in data.dict(exclude_unset=True).items():
            setattr(model, field, value)
        self.db.commit()
        self.db.refresh(model)
        return model

