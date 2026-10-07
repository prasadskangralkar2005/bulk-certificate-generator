from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routes.jobs import router as jobs_router
from .routes.certificates import router as certificates_router


# Create database tables if they don't already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="Backend API for bulk certificate generation",
    version="1.0.0"
)


# Register API routers.
app.include_router(jobs_router)
app.include_router(certificates_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }