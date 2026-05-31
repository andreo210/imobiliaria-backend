"""initial

Revision ID: 0001
Revises:
Create Date: 2026-05-31 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Usuario",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("senha", sa.String(1000), nullable=False),
        sa.Column("papel", sa.String(50), server_default="corretor"),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "Cliente",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("telefone", sa.String(20), nullable=True),
        sa.Column("observacao", sa.String(1000), nullable=True),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "TipoImovel",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("nome", sa.String(50), nullable=False),
    )

    op.create_table(
        "Amenidade",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("nome", sa.String(100), nullable=False),
    )

    op.create_table(
        "Imovel",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("titulo", sa.String(200), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("preco", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column(
            "status",
            sa.Enum("disponível", "vendido", "alugado", name="imovelstatus"),
            nullable=False,
        ),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("tipo_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tipo_id"], ["TipoImovel.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "RefreshToken",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(512), nullable=False),
        sa.Column("expiracao", sa.DateTime(), nullable=False),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["usuario_id"], ["Usuario.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "FotoImovel",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("url", sa.String(255), nullable=False),
        sa.Column("criado_em", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("imovel_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["imovel_id"], ["Imovel.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "ImovelAmenidade",
        sa.Column("imovel_id", sa.Integer(), primary_key=True),
        sa.Column("amenidade_id", sa.Integer(), primary_key=True),
        sa.ForeignKeyConstraint(["imovel_id"], ["Imovel.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["amenidade_id"], ["Amenidade.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("ImovelAmenidade")
    op.drop_table("FotoImovel")
    op.drop_table("RefreshToken")
    op.drop_table("Imovel")
    op.drop_table("Amenidade")
    op.drop_table("TipoImovel")
    op.drop_table("Cliente")
    op.drop_table("Usuario")

    op.execute("DROP TYPE IF EXISTS imovelstatus")
