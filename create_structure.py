import os
import sys

def create_directory_structure():
    """Create the complete directory structure for the blood analysis system"""
    
    print("🩸 Creating Blood Analysis System Directory Structure")
    print("=" * 50)
    
    # Main directories for backend
    directories = [
        'app',
        'app/models',
        'app/routes', 
        'app/services',
        'app/utils',
        'uploads',
        'ml_models',
        'logs'
    ]
    
    # Create directories
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}/")
        except Exception as e:
            print(f"❌ Failed to create {directory}: {e}")
    
    # Create __init__.py files
    init_files = [
        'app/__init__.py',
        'app/models/__init__.py',
        'app/routes/__init__.py',
        'app/services/__init__.py',
        'app/utils/__init__.py'
    ]
    
    for init_file in init_files:
        try:
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"✅ Created: {init_file}")
        except Exception as e:
            print(f"❌ Failed to create {init_file}: {e}")
    
    print("\n🎉 Backend directory structure created successfully!")
    print("\n📁 Backend Structure:")
    print("""
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── uploads/
├── ml_models/
├── logs/
└── all your Python files...
    """)
    
    print("\n🚀 Next Steps:")
    print("1. Run: python setup.py (to install dependencies)")
    print("2. Run: python init_database.py (to initialize database)")
    print("3. Run: python train_enhanced_model.py (to train ML model)")
    print("4. Run: python run.py (to start the server)")

if __name__ == "__main__":
    create_directory_structure()