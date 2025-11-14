import uvicorn
from app.main import app
from database import init_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('blood_analysis.log')
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Initialize database connection
        logger.info("🚀 Starting Blood Analysis System...")
        init_db()
        logger.info("✅ Database initialized successfully")
        
        # Start the server
        logger.info("🌐 Starting FastAPI server...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        raise