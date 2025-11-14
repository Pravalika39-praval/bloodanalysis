-- Create tablespace and user
CREATE TABLESPACE blood_analysis_ts
DATAFILE 'blood_analysis.dbf' SIZE 100M AUTOEXTEND ON;

CREATE USER blood_analysis_user IDENTIFIED BY daa
DEFAULT TABLESPACE blood_analysis_ts
QUOTA UNLIMITED ON blood_analysis_ts;

GRANT CONNECT, RESOURCE TO blood_analysis_user;

-- Connect as blood_analysis_user
-- Patients table
CREATE TABLE patients (
    patient_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER,
    name VARCHAR2(100) NOT NULL,
    age NUMBER,
    gender VARCHAR2(10),
    email VARCHAR2(100),
    phone VARCHAR2(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blood parameters table
CREATE TABLE blood_parameters (
    parameter_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parameter_name VARCHAR2(50) UNIQUE NOT NULL,
    normal_min NUMBER,
    normal_max NUMBER,
    unit VARCHAR2(20),
    category VARCHAR2(50)
);

-- Analysis results table
CREATE TABLE analysis_results (
    result_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    patient_id NUMBER REFERENCES patients(patient_id),
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    wbc NUMBER,
    rbc NUMBER,
    hgb NUMBER,
    hct NUMBER,
    mcv NUMBER,
    mch NUMBER,
    mchc NUMBER,
    plt NUMBER,
    rdw_sd NUMBER,
    rdw_cv NUMBER,
    pdw NUMBER,
    mpv NUMBER,
    p_lcr NUMBER,
    pct NUMBER,
    neut NUMBER,
    lymph NUMBER,
    mono NUMBER,
    eo NUMBER,
    baso NUMBER,
    ig NUMBER,
    nrbcs NUMBER,
    reticulocytes NUMBER,
    irf NUMBER,
    lfr NUMBER,
    mfr NUMBER,
    hfr NUMBER,
    severity_level VARCHAR2(20),
    risk_score NUMBER,
    raw_text CLOB
);

-- Diseases table
CREATE TABLE diseases (
    disease_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    disease_name VARCHAR2(100) NOT NULL,
    description CLOB,
    symptoms CLOB,
    prevention CLOB
);

-- Disease predictions table
CREATE TABLE disease_predictions (
    prediction_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    result_id NUMBER REFERENCES analysis_results(result_id),
    disease_id NUMBER REFERENCES diseases(disease_id),
    probability NUMBER,
    confidence_level VARCHAR2(20)
);

-- Recommendations table
CREATE TABLE recommendations (
    recommendation_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    disease_id NUMBER REFERENCES diseases(disease_id),
    category VARCHAR2(50),
    recommendation_text CLOB,
    duration_weeks NUMBER,
    priority_level VARCHAR2(20)
);

-- Users table
CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    full_name VARCHAR2(100),
    language_pref VARCHAR2(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis history table
CREATE TABLE analysis_history (
    history_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER REFERENCES users(user_id),
    result_id NUMBER REFERENCES analysis_results(result_id),
    analysis_type VARCHAR2(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);