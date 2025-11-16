from app.core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class RefreshToken(Base):
    __tablename__ = "RefreshToken"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Usuario.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(512), nullable=False)
    expiracao = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", backref="refresh_tokens")