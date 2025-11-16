from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class AmenidadeModel(Base):
    __tablename__ = "Amenidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

