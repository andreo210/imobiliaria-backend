from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.imovel_amenidade_association import imovel_amenidade_table

class AmenidadeModel(Base):
    __tablename__ = "Amenidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)

    # relação inversa com Imovel
    imoveis = relationship("ImovelModel",secondary=imovel_amenidade_table, back_populates="amenidades",lazy="raise")
