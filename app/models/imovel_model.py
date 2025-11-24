from app.core.database import Base
from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import relationship
from app.models.imovel_amenidade_association import imovel_amenidade_table
from sqlalchemy import Column, Enum as SqlEnum
from sqlalchemy import (Column,Integer,String,Text, DateTime, ForeignKey,Numeric)

class ImovelStatus(Enum):
    DISPONIVEL = "disponível"
    VENDIDO = "vendido"
    ALUGADO = "alugado"

class ImovelModel(Base):
    __tablename__ = "Imovel"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(200), nullable=False)
    descricao: str = Column(Text, nullable=True)
    preco = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(SqlEnum(ImovelStatus, name="imovelstatus"), nullable=False)
    criado_em: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    # chave estrangeira
    usuario_id: Optional[int] = Column(Integer, nullable=True)
    tipo_id: Optional[int] = Column(Integer, ForeignKey("TipoImovel.id"), nullable=True)

    # relações
    tipo = relationship("TipoImovelModel", back_populates="imoveis",lazy="raise")
    fotos = relationship("FotoImovelModel", back_populates="imovel", cascade="all, delete-orphan",lazy="raise")
    amenidades = relationship("AmenidadeModel",secondary=imovel_amenidade_table, back_populates="imoveis",lazy="raise")

    def __repr__(self) -> str:
        return f"<Imovel(id={self.id}, titulo={self.titulo}, preco={self.preco}, status={self.status})>"

