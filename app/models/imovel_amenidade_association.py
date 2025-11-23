from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

imovel_amenidade_table = Table(
    "ImovelAmenidade",
    Base.metadata,
    Column("imovel_id", Integer, ForeignKey("Imovel.id", ondelete="CASCADE"), primary_key=True),
    Column("amenidade_id", Integer, ForeignKey("Amenidade.id", ondelete="CASCADE"), primary_key=True),
)
