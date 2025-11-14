from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

# Import all route modules
from app.routes import auth, patients, analysis, translation  # ✅ Added translation here
from database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blood Analysis System API",
    description="Comprehensive blood report analysis with 26 parameters",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(analysis.router)
app.include_router(translation.router)  # ✅ Added translation router

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("ml_models", exist_ok=True)
os.makedirs("app/services", exist_ok=True)
os.makedirs("app/utils", exist_ok=True)
os.makedirs("static", exist_ok=True)  # ✅ for voice/audio files

# Mount static files (for uploads and generated audio)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")  # ✅ Added this line

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

@app.get("/")
async def root():
    return {
        "message": "🩸 Blood Analysis System API", 
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "blood-analysis-api",
        "database": "connected"
    }

@app.get("/api/info")
async def api_info():
    return {
        "name": "Blood Analysis System",
        "parameters_supported": 26,
        "diseases_detected": 13,
        "features": ["OCR", "ML Analysis", "Recommendations", "Multi-language", "Voice Output"]
    }
