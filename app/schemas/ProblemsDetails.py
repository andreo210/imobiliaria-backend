from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ProblemDetails404(BaseModel):
    type: str = "objeto não encontrado"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None

class ProblemDetails401(BaseModel):
    type: str = "não autorizado"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None

class ProblemDetails400(BaseModel):
    type: str = "bad request"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None