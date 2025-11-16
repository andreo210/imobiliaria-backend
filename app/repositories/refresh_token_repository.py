from sqlalchemy.orm import Session
from app.models.refresh_token_model import RefreshToken
from datetime import datetime

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, usuario_id: int, token: str, expiracao: datetime):
        rt = RefreshToken(usuario_id=usuario_id, token=token, expiracao=expiracao)
        self.db.add(rt)
        self.db.commit()
        self.db.refresh(rt)
        return rt

    def buscar(self, token: str, usuario_id: int):
        return self.db.query(RefreshToken).filter_by(token=token, usuario_id=usuario_id).first()

    def deletar(self, token: str):
        rt = self.db.query(RefreshToken).filter_by(token=token).first()
        if rt:
            self.db.delete(rt)
            self.db.commit()
