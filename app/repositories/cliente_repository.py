from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel

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
