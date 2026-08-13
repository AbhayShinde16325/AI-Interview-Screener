import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.genai import errors as genai_errors

from app.api.v1.auth import router as auth_router
from app.api.v1.evaluation import router as evaluation_router
from app.api.v1.interviews import router as interviews_router
from app.api.v1.resumes import router as resumes_router

from app.core.config import settings
from app.core.exceptions import (
    AppError,
    AuthenticationError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
    ValidationError,
)
from app.core.logging import setup_logging

setup_logging()

logger = logging.getLogger("app.main")

app = FastAPI(
    title="AI Interview Screener API",
    version="1.0.0",
    description=(
        "Role-based candidate screening with RAG: upload a resume, "
        "generate a grounded technical interview, and get an evaluation."
    ),
)

# --- CORS (the Vercel frontend talks to this API) -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Global exception handlers --------------------------------------------
@app.exception_handler(ResourceNotFoundError)
async def not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ResourceAlreadyExistsError)
async def conflict_handler(request: Request, exc: ResourceAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(AuthenticationError)
async def auth_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(genai_errors.ClientError)
async def gemini_error_handler(request: Request, exc: genai_errors.ClientError):
    """
    Surface Gemini API quota / rate-limit errors as a readable 429 instead
    of an opaque 500 (free-tier caps are easy to hit during testing).
    """
    if exc.code == 429:
        return JSONResponse(
            status_code=429,
            content={
                "detail": (
                    "The AI service rate limit or daily quota was reached. "
                    "Wait a few minutes (or until the daily limit resets) "
                    "and try again."
                )
            },
        )
    return JSONResponse(
        status_code=502,
        content={"detail": "The AI service returned an error. Please try again."},
    )


# --- Routers ---------------------------------------------------------------
app.include_router(auth_router, prefix="/api/v1")
app.include_router(resumes_router, prefix="/api/v1")
app.include_router(interviews_router, prefix="/api/v1")
app.include_router(evaluation_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "AI Interview Screener API is running."}


@app.get("/health")
def health():
    return {"status": "ok"}
