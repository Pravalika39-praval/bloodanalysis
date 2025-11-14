from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import text
import logging

from app.models.database_models import Patient, PatientCreate, User
from app.routes.auth import get_current_user
from database import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=Patient)
async def create_patient(patient: PatientCreate, current_user: User = Depends(get_current_user)):
    """Create new patient"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO patients (user_id, name, age, gender, email, phone)
                    VALUES (:user_id, :name, :age, :gender, :email, :phone)
                    RETURNING patient_id, created_at
                """),
                {
                    "user_id": current_user.user_id,
                    "name": patient.name,
                    "age": patient.age,
                    "gender": patient.gender,
                    "email": patient.email,
                    "phone": patient.phone
                }
            )
            patient_data = result.fetchone()
            conn.commit()
        
        logger.info(f"Patient created: {patient.name}")
        return Patient(
            patient_id=patient_data[0],
            name=patient.name,
            age=patient.age,
            gender=patient.gender,
            email=patient.email,
            phone=patient.phone,
            created_at=patient_data[1]
        )
    except Exception as e:
        logger.error(f"Create patient error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create patient"
        )

@router.get("/", response_model=List[Patient])
async def get_patients(current_user: User = Depends(get_current_user)):
    """Get all patients for current user"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("SELECT * FROM patients WHERE user_id = :user_id ORDER BY created_at DESC"),
                {"user_id": current_user.user_id}
            )
            patients = result.fetchall()
        
        return [
            Patient(
                patient_id=row[0],
                name=row[2],
                age=row[3],
                gender=row[4],
                email=row[5],
                phone=row[6],
                created_at=row[7]
            )
            for row in patients
        ]
    except Exception as e:
        logger.error(f"Get patients error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch patients"
        )

@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: int, current_user: User = Depends(get_current_user)):
    """Get specific patient"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("SELECT * FROM patients WHERE patient_id = :patient_id AND user_id = :user_id"),
                {"patient_id": patient_id, "user_id": current_user.user_id}
            )
            patient_data = result.fetchone()
        
        if not patient_data:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return Patient(
            patient_id=patient_data[0],
            name=patient_data[2],
            age=patient_data[3],
            gender=patient_data[4],
            email=patient_data[5],
            phone=patient_data[6],
            created_at=patient_data[7]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get patient error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch patient"
        )