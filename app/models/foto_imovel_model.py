from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from app.core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class FotoImovelModel(Base):
    __tablename__ = "FotoImovel"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String(255), nullable=False)
    criado_em: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    # chave estrangeira
    imovel_id: int = Column(Integer, ForeignKey("Imovel.id", ondelete="CASCADE"), nullable=False)
    # relação
    imovel = relationship("ImovelModel", back_populates="fotos", lazy="raise")

    def __repr__(self) -> str:
        return f"<FotoImovel(id={self.id}, imovel_id={self.imovel_id}, url={self.url})>"