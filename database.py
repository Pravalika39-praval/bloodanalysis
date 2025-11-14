import oracledb
from contextlib import contextmanager
from config import config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.dsn = f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
        logger.info(f"Database DSN: {self.dsn}")
    
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = oracledb.connect(
                user=config.DB_USERNAME,
                password=config.DB_PASSWORD,
                dsn=self.dsn
            )
            logger.info("✅ Database connection established")
            yield connection
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
        finally:
            if connection:
                connection.close()
                logger.debug("Database connection closed")

# Global database instance
db = Database()

def init_db():
    """Initialize database connection and verify"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            if result and result[0] == 1:
                logger.info("✅ Database connection verified successfully")
            else:
                raise Exception("Database verification failed")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise