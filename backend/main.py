from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from database import engine, Base
from config import get_settings

# Import routers
from routers import auth, routers, network, metrics, websocket

# Import background services
from services.monitoring_service import monitor_routers

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    This runs when the application starts and stops.
    We use it to start the background monitoring task.
    """
    # Startup: Start background monitoring
    print("🚀 Starting background monitoring service...")
    monitoring_task = asyncio.create_task(monitor_routers())
    
    yield
    
    # Shutdown: Cancel background tasks
    print("🛑 Stopping background monitoring service...")
    monitoring_task.cancel()
    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass


# Create FastAPI application
app = FastAPI(
    title="Network Monitor API",
    description="Real-time network monitoring API for routers with BGP, OSPF, and interface tracking",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
allowed_origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(routers.router)
app.include_router(network.router)
app.include_router(metrics.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Network Monitor API v2.0 is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
