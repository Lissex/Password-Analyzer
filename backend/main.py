from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine

from src.infrastructure.database.connection import settings
from src.infrastructure.database.models import Base
from src.presentation.api.v1 import router as api_router


async def run_migrations():
    """Run alembic migrations programmatically on startup"""
    try:
        from alembic.config import Config
        from alembic import command
        
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully")
    except Exception as e:
        print(f"Warning: Could not run migrations: {e}")
        print("Make sure you've run: alembic revision --autogenerate -m 'init' && alembic upgrade head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    print("Starting up...")
    # Uncomment this after creating first migration
    # await run_migrations()
    print("Starting up complete")
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Password Analyzer API",
    description="A password analysis tool with entropy calculation and crack time estimation",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

# Serve static files (frontend)
# frontend_path = Path(__file__).parent.parent / "frontend"
# if frontend_path.exists():
#     app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
# else:
#     print(f"Warning: Frontend directory not found at {frontend_path}")

frontend_path = Path("/app/frontend")
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")
    
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "password-analyzer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )