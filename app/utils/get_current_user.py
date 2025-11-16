from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

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
