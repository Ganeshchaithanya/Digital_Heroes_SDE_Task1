"""
PAGEPULSE FastAPI Main Application Entrypoint.
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.inspect import router as v1_router
from app.observability.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="PAGEPULSE - Deterministic Website Inspection Platform with AI Summary Insights.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for Frontend development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(v1_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "online",
        "health_check": "/health",
        "api_docs": "/docs",
        "inspect_endpoint": f"{settings.API_V1_STR}/inspect"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting PAGEPULSE Uvicorn Development Server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
