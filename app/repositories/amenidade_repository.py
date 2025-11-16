from sqlalchemy.orm import Session
from app.models.amenidade_model import AmenidadeModel

class AmenidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, amenidade: AmenidadeModel):
        self.db.add(amenidade)
        self.db.commit()
        self.db.refresh(amenidade)
        return amenidade

    def get_all(self):
        return self.db.query(AmenidadeModel).all()

    def get_by_id(self, id: int):
        return self.db.query(AmenidadeModel).filter(AmenidadeModel.id == id).first()


    def delete(self, id: int):
        amenidade = self.db.query(AmenidadeModel).filter(AmenidadeModel.id == id).first()
        if amenidade:
            self.db.delete(amenidade)
            self.db.commit()
            return amenidade
        return None
