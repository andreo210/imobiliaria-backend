"""from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests

security = HTTPBearer()

# URL do realm do Keycloak
KEYCLOAK_URL = "http://localhost:8080/realms/meu_realm"
ALGORITHM = "RS256"

# Buscar chave pública do Keycloak
def get_keycloak_public_key():
    resp = requests.get(f"{KEYCLOAK_URL}/protocol/openid-connect/certs")
    jwks = resp.json()
    return jwks  # conjunto de chaves públicas

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # decodifica usando chave pública do Keycloak
        jwks = get_keycloak_public_key()
        payload = jwt.decode(token, jwks, algorithms=[ALGORITHM])

        return {
            "id": payload.get("sub"),
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", [])
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")"""
