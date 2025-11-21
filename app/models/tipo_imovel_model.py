from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class TipoImovelModel(Base):
    __tablename__ = "TipoImovel"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)

