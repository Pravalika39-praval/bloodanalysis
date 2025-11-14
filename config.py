import os
from typing import Dict, Any

class Config:
    # Database Configuration - Oracle
    DB_USERNAME = 'system'
    DB_PASSWORD = 'system'
    DB_HOST = 'localhost'
    DB_PORT = '1521'
    DB_SERVICE = 'XE'
    
    # ✅ Use python-oracledb connection string
    @property
    def DATABASE_URL(self):
        return f"oracle+oracledb://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_SERVICE}"
    
    # JWT Configuration
    SECRET_KEY = 'blood-analysis-secret-key-2024-change-in-production-very-secure'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    
    # OCR Configuration
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # ML Models Configuration
    MODEL_PATH = 'ml_models/'
    MODEL_FILE = 'enhanced_blood_model.pkl'
    
    # Dataset path
    DATASET_PATH = r'C:\Users\ardha\Downloads\combine'
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'hi', 'zh', 'te', 'ta']
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG = True

# Global config instance
config = Config()