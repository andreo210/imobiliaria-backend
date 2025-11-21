from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.repositories.refresh_token_repository import RefreshTokenRepository
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    def criar_tokens(self, usuario):
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
        self.repo.salvar(
            usuario.id,
            refresh_token,
            datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return access_token, refresh_token

    def refresh_tokens(self, refresh_token: str, usuario_id: int, nome: str, email: str, papel: str):
        token_db = self.repo.buscar(refresh_token, usuario_id)
        if not token_db or token_db.expiracao < datetime.utcnow():
            return None

        # recria tokens com claims completas
        usuario_fake = type("UsuarioFake", (), {
            "id": usuario_id,
            "nome": nome,
            "email": email,
            "papel": papel
        })()
        return self.criar_tokens(usuario_fake)

    def logout(self, refresh_token: str):
        self.repo.deletar(refresh_token)

    def validar_refresh_token(self,refresh_token: str):
        try:
            # decodifica o token usando a chave secreta e algoritmo teste
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

            usuario_id = payload.get("sub")
            nome = payload.get("nome")
            email = payload.get("email")
            papel = payload.get("papel")

            if usuario_id is None or email is None:
                raise JWTError("Token inválido: faltam claims obrigatórias")

            # retorna as claims para uso posterior
            return {
                "sub": usuario_id,
                "nome": nome,
                "email": email,
                "papel": papel
            }

        except JWTError:
            # token inválido ou expirado
            return None



