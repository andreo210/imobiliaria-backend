from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.repositories.refresh_token_repository import RefreshTokenRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthService:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo


    async def criar_tokens(self,db: AsyncSession, usuario):
        # claims extras: nome e email
        data = {
            "sub": str(usuario.id),
            "nome": usuario.nome,
            "email": usuario.email,
            "papel": usuario.papel
        }

        access_token = jwt.encode(
            {**data, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY, algorithm=ALGORITHM
        )

        refresh_token = jwt.encode(
            {**data, "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)},
            SECRET_KEY, algorithm=ALGORITHM
        )

        # salva refresh token no banco
        await self.repo.salvar(
            usuario.id,
            refresh_token,
            datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            db
        )

        return access_token, refresh_token

    async def refresh_tokens(self,db: AsyncSession, refresh_token: str, usuario_id: int, nome: str, email: str, papel: str):
        token_db = await self.repo.buscar(refresh_token, usuario_id,db)
        if not token_db or token_db.expiracao < datetime.utcnow():
            return None

        # recria tokens com claims completas
        usuario_fake = type("UsuarioFake", (), {
            "id": usuario_id,
            "nome": nome,
            "email": email,
            "papel": papel
        })()
        return await self.criar_tokens(db,usuario_fake)

    async def logout(self, db: AsyncSession, refresh_token: str):
        await self.repo.deletar(db, refresh_token)

    async def validar_refresh_token(self, db: AsyncSession, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id = payload.get("sub")
            nome = payload.get("nome")
            email = payload.get("email")
            papel = payload.get("papel")

            if usuario_id is None or email is None:
                raise JWTError("Token inválido: faltam claims obrigatórias")

            return {
                "sub": usuario_id,
                "nome": nome,
                "email": email,
                "papel": papel
            }
        except JWTError:
            return None



