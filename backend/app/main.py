from fastapi import FastAPI
from app.api.v1.resumes import router as resumes_router
from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="AI Interview Screener API",
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "AI Interview Screener API is running."
    }

app.include_router(
    resumes_router,
    prefix="/api/v1",
)