import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from alembic import context

from app.core.database import Base
from app.models.usuario_model import Usuario
from app.models.cliente_model import ClienteModel
from app.models.tipo_imovel_model import TipoImovelModel
from app.models.imovel_model import ImovelModel
from app.models.foto_imovel_model import FotoImovelModel
from app.models.amenidade_model import AmenidadeModel
from app.models.refresh_token_model import RefreshToken
from app.models.imovel_amenidade_association import imovel_amenidade_table

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://root:Taina2011.@localhost:3306/imobiliaria"
)


def run_migrations_offline() -> None:
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
