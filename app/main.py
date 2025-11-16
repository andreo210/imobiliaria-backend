from fastapi import FastAPI
from app.routers import usuario_router, amenidade_router, auth_router  # importar outros routers depois
from app.routers import cliente_router
from starlette.requests import Request
from app.schemas.ProblemsDetails import ProblemDetails404
from fastapi.responses import JSONResponse
app = FastAPI(title="API Imobiliária")

app.include_router(usuario_router.router)
app.include_router(auth_router.router)
app.include_router(cliente_router.router)
app.include_router(amenidade_router.router)
# app.include_router(contrato.router)
# app.include_router(pagamento.router)




@app.exception_handler(Exception)
async def problem_details_handler(request: Request, exc: Exception):
    problem = ProblemDetails404(
        title="erro interno",
        status=500,
        detail=str(exc),
        instance=str(request.url),
    )
    return JSONResponse(status_code=500, content=problem.dict())