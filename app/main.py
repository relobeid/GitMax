from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from app.utils.config import get_settings
from app.database import create_tables
from app.routers import auth, profile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get application settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="GitMax API",
    description="GitHub-based career coaching platform API",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler.
    
    Args:
        request: The request object.
        exc: The exception.
        
    Returns:
        JSONResponse: The error response.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: Welcome message.
    """
    return {
        "message": "Welcome to GitMax API",
        "docs": "/docs",
    }


# Health check endpoint
@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status.
    """
    return {"status": "ok"}


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Startup event.
    """
    logger.info("Starting up GitMax API")
    create_tables()


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event.
    """
    logger.info("Shutting down GitMax API")


# Run the application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
