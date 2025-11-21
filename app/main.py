from fastapi import FastAPI
from app.routers import usuario_router, amenidade_router, auth_router ,tipo_imovel_router # importar outros routers depois
from app.routers import cliente_router
from starlette.requests import Request
from app.schemas.ProblemsDetails import ProblemDetails404
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="API Imobiliária")

app.include_router(tipo_imovel_router.router)
app.include_router(usuario_router.router)
app.include_router(auth_router.router)
app.include_router(cliente_router.router)
app.include_router(amenidade_router.router)
# app.include_router(contrato.router)
# app.include_router(pagamento.router)

# Defina as origens permitidas
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ou ["*"] para liberar tudo
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],            # Autorize todos os headers
)


@app.exception_handler(Exception)
async def problem_details_handler(request: Request, exc: Exception):
    problem = ProblemDetails404(
        title="erro interno",
        status=500,
        detail=str(exc),
        instance=str(request.url),
    )
    return JSONResponse(status_code=500, content=problem.dict())