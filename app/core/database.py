from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://root:Taina2011.@localhost:3306/imobiliaria"
)

Base = declarative_base()


def get_engine():
    return create_async_engine(DATABASE_URL, echo=True)


def get_session_local():
    engine = get_engine()
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )


async def get_db() -> AsyncSession:
    async with get_session_local()() as session:
        yield session
