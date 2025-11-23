from sqlalchemy.orm import Session
from app.models.tipo_imovel_model import TipoImovelModel

class TipoImovelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TipoImovelModel).all()

    def get_by_id(self, id: int):
        return self.db.query(TipoImovelModel).filter(TipoImovelModel.id == id).first()



