import oracledb
from config import config
import sys

def init_database():
    try:
        print("Blood Analysis System - Database Initialization")
        print("=" * 50)
        
        # Test database connection
        print("🔍 Testing database connection...")
        
        # Use python-oracledb (much easier installation)
        connection = oracledb.connect(
            user=config.DB_USERNAME,
            password=config.DB_PASSWORD,
            dsn=f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_SERVICE}"
        )
        
        print("✅ Database connection established!")
        print(f"Oracle Version: {connection.version}")
        
        cursor = connection.cursor()
        
        # Create tables (same as before)
        print("Creating tables...")
        
        # Patients table
        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE patients CASCADE CONSTRAINTS';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """)
        
        cursor.execute("""
            CREATE TABLE patients (
                patient_id VARCHAR2(20) PRIMARY KEY,
                name VARCHAR2(100) NOT NULL,
                age NUMBER,
                gender VARCHAR2(10),
                contact_number VARCHAR2(15),
                email VARCHAR2(100),
                address CLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Patients table created")
        
        # Blood test results table
        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE blood_test_results CASCADE CONSTRAINTS';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """)
        
        cursor.execute("""
            CREATE TABLE blood_test_results (
                result_id VARCHAR2(20) PRIMARY KEY,
                patient_id VARCHAR2(20) REFERENCES patients(patient_id),
                test_date DATE DEFAULT SYSDATE,
                hemoglobin NUMBER,
                wbc_count NUMBER,
                rbc_count NUMBER,
                platelets NUMBER,
                glucose NUMBER,
                cholesterol NUMBER,
                alt NUMBER,
                ast NUMBER,
                bilirubin NUMBER,
                creatinine NUMBER,
                bun NUMBER,
                sodium_level NUMBER,
                potassium_level NUMBER,
                test_type VARCHAR2(50),
                lab_notes CLOB,
                ocr_raw_data CLOB,
                confidence_score NUMBER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Blood test results table created")
        
        # Users table
        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE users CASCADE CONSTRAINTS';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """)
        
        cursor.execute("""
            CREATE TABLE users (
                user_id VARCHAR2(20) PRIMARY KEY,
                username VARCHAR2(50) UNIQUE NOT NULL,
                email VARCHAR2(100) UNIQUE NOT NULL,
                hashed_password VARCHAR2(255) NOT NULL,
                full_name VARCHAR2(100),
                role VARCHAR2(20) DEFAULT 'user',
                is_active NUMBER(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Users table created")
        
        # Insert sample data (same as before)
        print("Inserting sample data...")
        
        sample_patients = [
            ('P-001', 'John Smith', 45, 'Male', '+1234567890', 'john.smith@email.com', '123 Main St, City'),
            ('P-002', 'Maria Garcia', 32, 'Female', '+0987654321', 'maria.garcia@email.com', '456 Oak Ave, Town'),
            ('P-003', 'Robert Johnson', 58, 'Male', '+1122334455', 'robert.johnson@email.com', '789 Pine Rd, Village')
        ]
        
        cursor.executemany("""
            INSERT INTO patients (patient_id, name, age, gender, contact_number, email, address)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, sample_patients)
        
        connection.commit()
        print("✅ Sample data inserted")
        
        connection.close()
        print("✅ Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()