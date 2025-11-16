from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.refresh_token_schema import LoginRequest, TokenResponse, RefreshRequest
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.core.database import get_db  # função que retorna a sessão do SQLAlchemy

router = APIRouter(prefix="/auth", tags=["auth"])

# rota de login
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario_repo = UsuarioRepository(db)
    usuario_service = UsuarioService(usuario_repo)

    usuario = usuario_service.autenticar(request.email, request.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    refresh_repo = RefreshTokenRepository(db)
    auth_service = AuthService(refresh_repo)

    access_token, refresh_token = auth_service.criar_tokens(usuario)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# rota de refresh
@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    refresh_repo = RefreshTokenRepository(db)
    auth_service = AuthService(refresh_repo)

    try:
        # decodifica o refresh token e gera novos tokens
        payload = auth_service.validar_refresh_token(request.refresh_token)
        usuario_id = payload.get("sub")
        papel = payload.get("papel")
        nome = payload.get("nome")
        email = payload.get("email")

        tokens = auth_service.refresh_tokens(request.refresh_token, usuario_id,nome,email, papel)
        if not tokens:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

        access_token, new_refresh_token = tokens
        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

# rota de logout
@router.post("/logout")
def logout(request: RefreshRequest, db: Session = Depends(get_db)):
    refresh_repo = RefreshTokenRepository(db)
    auth_service = AuthService(refresh_repo)

    auth_service.logout(request.refresh_token)
    return {"detail": "Logout realizado com sucesso"}
