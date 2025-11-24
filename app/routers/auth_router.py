from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.refresh_token_schema import LoginRequest, TokenResponse, RefreshRequest
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


# rota de login
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    usuario_repo = UsuarioRepository()
    usuario_service = UsuarioService(usuario_repo)

    usuario = await usuario_service.autenticar(db, request.email, request.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    refresh_repo = RefreshTokenRepository()
    auth_service = AuthService(refresh_repo)

    access_token, refresh_token = await auth_service.criar_tokens(db, usuario)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# rota de refresh
@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    refresh_repo = RefreshTokenRepository()
    auth_service = AuthService(refresh_repo)

    try:
        payload = await auth_service.validar_refresh_token(db, request.refresh_token)
        usuario_id = payload.get("sub")
        papel = payload.get("papel")
        nome = payload.get("nome")
        email = payload.get("email")

        tokens = await auth_service.refresh_tokens(db, request.refresh_token, usuario_id, nome, email, papel)
        if not tokens:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

        access_token, new_refresh_token = tokens
        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")


# rota de logout
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    refresh_repo = RefreshTokenRepository()
    auth_service = AuthService(refresh_repo)

    await auth_service.logout(db, request.refresh_token)
    return {"detail": "Logout realizado com sucesso"}
