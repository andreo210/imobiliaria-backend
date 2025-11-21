from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioBase

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def create(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get_all(self):
        return self.db.query(Usuario).all()

    def get_by_id(self, id: int):
        return self.db.query(Usuario).filter(Usuario.id == id).first()

    def delete(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()

    def update(self, id: int, data: UsuarioBase):
        model = self.get_by_id(id)
        if not model:
            return None
        # Atualiza apenas os campos enviados
        for field, value in data.dict(exclude_unset=True).items():
            setattr(model, field, value)
        self.db.commit()
        self.db.refresh(model)
        return model