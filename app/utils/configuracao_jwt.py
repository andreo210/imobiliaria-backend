from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "teste"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        nome = payload.get("nome")
        email = payload.get("email")
        papel = payload.get("papel")

        if usuario_id is None or email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return {
            "id": usuario_id,
            "nome": nome,
            "email": email,
            "papel": papel
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
