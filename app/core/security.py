from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "sua_chave_super_secreta"
ALGORITHM = "HS256"

security =  HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # aqui você pega a string JWT
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
