from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class ClienteModel(Base):
    __tablename__ = "Cliente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100),unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
