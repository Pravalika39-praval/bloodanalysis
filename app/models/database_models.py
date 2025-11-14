from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    language_pref: str = 'en'

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PatientCreate(PatientBase):
    user_id: Optional[int] = None  # Will be set from current user

class Patient(PatientBase):
    patient_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BloodParameters(BaseModel):
    wbc: Optional[float] = None
    rbc: Optional[float] = None
    hgb: Optional[float] = None
    hct: Optional[float] = None
    mcv: Optional[float] = None
    mch: Optional[float] = None
    mchc: Optional[float] = None
    plt: Optional[float] = None
    rdw_sd: Optional[float] = None
    rdw_cv: Optional[float] = None
    pdw: Optional[float] = None
    mpv: Optional[float] = None
    p_lcr: Optional[float] = None
    pct: Optional[float] = None
    neut: Optional[float] = None
    lymph: Optional[float] = None
    mono: Optional[float] = None
    eo: Optional[float] = None
    baso: Optional[float] = None
    ig: Optional[float] = None
    nrbcs: Optional[float] = None
    reticulocytes: Optional[float] = None
    irf: Optional[float] = None
    lfr: Optional[float] = None
    mfr: Optional[float] = None
    hfr: Optional[float] = None

class AnalysisResultCreate(BloodParameters):
    patient_id: int
    raw_text: Optional[str] = None

class AnalysisResult(AnalysisResultCreate):
    result_id: int
    analysis_date: datetime
    severity_level: Optional[str] = None
    risk_score: Optional[float] = None
    
    class Config:
        from_attributes = True

class DiseasePrediction(BaseModel):
    disease_name: str
    probability: float
    confidence_level: str
    description: Optional[str] = None
    symptoms: Optional[str] = None
    prevention: Optional[str] = None

class Recommendation(BaseModel):
    category: str
    recommendation_text: str
    duration_weeks: int
    priority_level: str

class AnalysisResponse(BaseModel):
    result_id: int
    parameters: BloodParameters
    disease_predictions: List[DiseasePrediction]
    severity_level: str
    risk_score: float
    recommendations: List[Recommendation]
    normal_ranges: Dict[str, Any]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None