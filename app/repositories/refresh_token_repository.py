from sqlalchemy.orm import Session
from app.models.refresh_token_model import RefreshToken
from datetime import datetime
from app.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self):
        super().__init__(RefreshToken)

    async def salvar(self, usuario_id: int, token: str, expiracao: datetime,db: AsyncSession):
        rt = RefreshToken(usuario_id=usuario_id, token=token, expiracao=expiracao)
        db.add(rt)
        await db.commit()
        await db.refresh(rt)
        return rt

    async def buscar(self, token: str, usuario_id: int, db: AsyncSession):
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.usuario_id == usuario_id
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def deletar(self, db: AsyncSession, token: str):
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        result = await db.execute(stmt)
        rt = result.scalar_one_or_none()

        if rt:
            await db.delete(rt)
            await db.commit()
            return True
        return False
