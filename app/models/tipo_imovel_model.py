from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship

class TipoImovelModel(Base):
    __tablename__ = "TipoImovel"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)

    # relação opcional para ver os imóveis daquele tipo
    imoveis = relationship("ImovelModel", back_populates="tipo",lazy="raise")