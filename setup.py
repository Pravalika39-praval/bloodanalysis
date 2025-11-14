import os
import subprocess
import sys
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install all required packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def download_spacy_model():
    """Download spaCy model"""
    print("🔤 Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download spaCy model: {e}")
        return False

def check_system_dependencies():
    """Check for system dependencies"""
    print("🔍 Checking system dependencies...")
    
    # Check Tesseract
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        else:
            result = subprocess.run(["which", "tesseract"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tesseract OCR found")
            if platform.system() == "Windows":
                print(f"   Tesseract path: {result.stdout.split()[1]}")
        else:
            print("❌ Tesseract OCR not found. Please install:")
            if platform.system() == "Windows":
                print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
                print("   Default install path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
            elif platform.system() == "Linux":
                print("   Run: sudo apt install tesseract-ocr")
            elif platform.system() == "Darwin":
                print("   Run: brew install tesseract")
    except Exception as e:
        print(f"⚠️  Could not check Tesseract: {e}")

def check_oracle_connection():
    """Check Oracle database connection"""
    print("🗄️  Checking Oracle database configuration...")
    try:
        # Try to import oracledb to check if it's installed
        import oracledb
        print("✅ oracledb package is installed")
        
        # Check if config exists and has database settings
        try:
            from config import config
            if hasattr(config, 'DB_USERNAME') and hasattr(config, 'DB_PASSWORD'):
                print("✅ Database configuration found in config.py")
                print(f"   Username: {config.DB_USERNAME}")
                print(f"   Host: {config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}")
            else:
                print("❌ Database configuration missing in config.py")
        except ImportError:
            print("❌ config.py not found or invalid")
            
    except ImportError:
        print("❌ oracledb package not installed")

def create_default_files():
    """Create default files if they don't exist"""
    print("📄 Checking essential files...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found - creating default...")
        requirements_content = """fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
oracledb==2.0.0
pydantic==2.5.0
pytesseract==0.3.10
pdf2image==1.16.3
Pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.2
xgboost==2.0.0
joblib==1.3.2
spacy==3.7.2
requests==2.31.0
python-magic==0.4.27
scipy==1.11.3
python-dateutil==2.8.2
sqlalchemy==2.0.23
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        print("✅ Created requirements.txt")
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ config.py not found - creating default...")
        config_content = '''import os

class Config:
    # Database Configuration - Oracle
    DB_USERNAME = 'system'
    DB_PASSWORD = 'daa'
    DB_HOST = 'localhost'
    DB_PORT = '1521'
    DB_SERVICE = 'XE'
    
    # JWT Configuration
    SECRET_KEY = 'blood-analysis-secret-key-2024-change-in-production-very-secure'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    
    # OCR Configuration
    TESSERACT_PATH = r'C:\\\\Program Files\\\\Tesseract-OCR\\\\tesseract.exe'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # ML Models Configuration
    MODEL_PATH = 'ml_models/'
    MODEL_FILE = 'enhanced_blood_model.pkl'
    
    # Dataset path
    DATASET_PATH = r'C:\\\\Users\\\\ardha\\\\Downloads\\\\combine'
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'hi', 'zh', 'te', 'ta']
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    DEBUG = True

config = Config()
'''
        with open('config.py', 'w') as f:
            f.write(config_content)
        print("✅ Created config.py with default settings")

def main():
    print("🩸 Blood Analysis System - Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create default files
    create_default_files()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Some dependencies may not have installed correctly")
    
    # Download spaCy model
    download_spacy_model()
    
    # Check system dependencies
    check_system_dependencies()
    
    # Check Oracle configuration
    check_oracle_connection()
    
    print("\n🎉 Backend setup completed!")
    print("\n📝 Next steps (run these in order):")
    print("1. python init_database.py          - Initialize database")
    print("2. python train_enhanced_model.py   - Train ML model with your blood reports")
    print("3. python run.py                    - Start the backend server")
    print("\n💡 Important Notes:")
    print("   • Make sure Oracle database is running")
    print("   • Update TESSERACT_PATH in config.py if needed")
    print("   • Backend will run on: http://192.168.0.132:8000")
    print("   • API docs will be at: http://192.168.0.132:8000/docs")

if __name__ == "__main__":
    main()