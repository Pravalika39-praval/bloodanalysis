from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from typing import List, Dict, Any
import logging
import os
from sqlalchemy import text

from app.models.database_models import AnalysisResponse, AnalysisResult, User, BloodParameters
from app.routes.auth import get_current_user
from app.services.ocr_service import OCRService
from app.services.nlp_extractor import NLPExtractor
from app.services.ml_models import BloodAnalysisModel
from app.services.recommendation_engine import RecommendationEngine
from app.services.translation_service import TranslationService
from app.utils.file_handlers import FileHandler
from app.models.blood_config import NORMAL_RANGES
from config import config
from database import db

router = APIRouter(prefix="/analysis", tags=["analysis"])
logger = logging.getLogger(__name__)

# Initialize services
ocr_service = OCRService(config.TESSERACT_PATH)
nlp_extractor = NLPExtractor()
ml_model = BloodAnalysisModel()
recommendation_engine = RecommendationEngine()
translation_service = TranslationService()
file_handler = FileHandler(config.UPLOAD_FOLDER)

@router.post("/upload", response_model=Dict[str, Any])
async def upload_blood_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload blood report file"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Validate file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > config.MAX_CONTENT_LENGTH:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save uploaded file
        file_path = await file_handler.save_upload_file(file)
        
        # Schedule cleanup
        background_tasks.add_task(file_handler.cleanup_file, file_path)
        
        return {
            "message": "File uploaded successfully",
            "file_path": file_path,
            "file_type": file_handler.get_file_type(file.filename),
            "file_size": file_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_blood_report(
    analysis_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Analyze blood report and provide predictions"""
    try:
        file_path = analysis_data.get('file_path')
        patient_id = analysis_data.get('patient_id')
        language = analysis_data.get('language', 'en')
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File path required or file not found")
        
        logger.info(f"Starting analysis for file: {file_path}")
        
        # Extract text from file
        file_type = file_handler.get_file_type(file_path)
        extracted_text = ocr_service.extract_text_from_file(file_path, file_type)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="No text extracted from file")
        
        # Clean and process text
        cleaned_text = nlp_extractor.clean_extracted_text(extracted_text)
        
        # Extract parameters using NLP
        parameters = nlp_extractor.extract_parameters(cleaned_text)
        validated_parameters = nlp_extractor.validate_parameters(parameters)
        
        if not validated_parameters:
            raise HTTPException(status_code=400, detail="No valid parameters found in report")
        
        logger.info(f"Extracted {len(validated_parameters)} parameters")
        
        # Save analysis results
        with db.get_connection() as conn:
            # Create patient record if not exists
            if not patient_id:
                result = conn.execute(
                    text("""
                        INSERT INTO patients (user_id, name) 
                        VALUES (:user_id, 'Anonymous Patient')
                        RETURNING patient_id
                    """),
                    {"user_id": current_user.user_id}
                )
                patient_id = result.fetchone()[0]
                logger.info(f"Created anonymous patient with ID: {patient_id}")
            
            # Save analysis results
            result = conn.execute(
                text("""
                    INSERT INTO analysis_results 
                    (patient_id, raw_text, wbc, rbc, hgb, hct, mcv, mch, mchc, plt, 
                     rdw_sd, rdw_cv, pdw, mpv, p_lcr, pct, neut, lymph, mono, eo, 
                     baso, ig, nrbcs, reticulocytes, irf, lfr, mfr, hfr)
                    VALUES (:patient_id, :raw_text, :wbc, :rbc, :hgb, :hct, :mcv, :mch, :mchc, :plt,
                            :rdw_sd, :rdw_cv, :pdw, :mpv, :p_lcr, :pct, :neut, :lymph, :mono, :eo,
                            :baso, :ig, :nrbcs, :reticulocytes, :irf, :lfr, :mfr, :hfr)
                    RETURNING result_id, analysis_date
                """),
                {
                    "patient_id": patient_id, 
                    "raw_text": cleaned_text,
                    "wbc": validated_parameters.get('WBC'),
                    "rbc": validated_parameters.get('RBC'),
                    "hgb": validated_parameters.get('HGB'),
                    "hct": validated_parameters.get('HCT'),
                    "mcv": validated_parameters.get('MCV'),
                    "mch": validated_parameters.get('MCH'),
                    "mchc": validated_parameters.get('MCHC'),
                    "plt": validated_parameters.get('PLT'),
                    "rdw_sd": validated_parameters.get('RDW_SD'),
                    "rdw_cv": validated_parameters.get('RDW_CV'),
                    "pdw": validated_parameters.get('PDW'),
                    "mpv": validated_parameters.get('MPV'),
                    "p_lcr": validated_parameters.get('P_LCR'),
                    "pct": validated_parameters.get('PCT'),
                    "neut": validated_parameters.get('NEUT'),
                    "lymph": validated_parameters.get('LYMPH'),
                    "mono": validated_parameters.get('MONO'),
                    "eo": validated_parameters.get('EO'),
                    "baso": validated_parameters.get('BASO'),
                    "ig": validated_parameters.get('IG'),
                    "nrbcs": validated_parameters.get('NRBCS'),
                    "reticulocytes": validated_parameters.get('RETICULOCYTES'),
                    "irf": validated_parameters.get('IRF'),
                    "lfr": validated_parameters.get('LFR'),
                    "mfr": validated_parameters.get('MFR'),
                    "hfr": validated_parameters.get('HFR')
                }
            )
            
            result_data = result.fetchone()
            result_id = result_data[0]
            analysis_date = result_data[1]
            conn.commit()
        
        logger.info(f"Analysis results saved with ID: {result_id}")
        
        # Get disease predictions
        disease_predictions_raw = ml_model.predict(validated_parameters)
        
        # Convert to disease format with severity
        disease_list = []
        for disease_name, probability in disease_predictions_raw:
            severity = _determine_disease_severity(disease_name, probability, validated_parameters)
            disease_list.append({
                'disease_name': disease_name,
                'probability': probability,
                'confidence_level': _get_confidence_level(probability),
                'severity': severity
            })
        
        # Calculate overall risk score
        risk_score = _calculate_risk_score(disease_list, validated_parameters)
        severity_level = _determine_severity(risk_score)
        
        # Update risk score in database
        with db.get_connection() as conn:
            conn.execute(
                text("""
                    UPDATE analysis_results 
                    SET severity_level = :severity_level, risk_score = :risk_score
                    WHERE result_id = :result_id
                """),
                {
                    "severity_level": severity_level,
                    "risk_score": risk_score,
                    "result_id": result_id
                }
            )
            conn.commit()
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(disease_list, validated_parameters)
        
        # Translate content if needed
        if language != 'en':
            for disease in disease_list:
                disease['disease_name'] = translation_service.translate_text(
                    disease['disease_name'], language
                )
            for rec in recommendations:
                rec['recommendation_text'] = translation_service.translate_text(
                    rec['recommendation_text'], language
                )
        
        # Prepare response
        blood_params = BloodParameters(**{
            'wbc': validated_parameters.get('WBC'),
            'rbc': validated_parameters.get('RBC'),
            'hgb': validated_parameters.get('HGB'),
            'hct': validated_parameters.get('HCT'),
            'mcv': validated_parameters.get('MCV'),
            'mch': validated_parameters.get('MCH'),
            'mchc': validated_parameters.get('MCHC'),
            'plt': validated_parameters.get('PLT'),
            'rdw_sd': validated_parameters.get('RDW_SD'),
            'rdw_cv': validated_parameters.get('RDW_CV'),
            'pdw': validated_parameters.get('PDW'),
            'mpv': validated_parameters.get('MPV'),
            'p_lcr': validated_parameters.get('P_LCR'),
            'pct': validated_parameters.get('PCT'),
            'neut': validated_parameters.get('NEUT'),
            'lymph': validated_parameters.get('LYMPH'),
            'mono': validated_parameters.get('MONO'),
            'eo': validated_parameters.get('EO'),
            'baso': validated_parameters.get('BASO'),
            'ig': validated_parameters.get('IG'),
            'nrbcs': validated_parameters.get('NRBCS'),
            'reticulocytes': validated_parameters.get('RETICULOCYTES'),
            'irf': validated_parameters.get('IRF'),
            'lfr': validated_parameters.get('LFR'),
            'mfr': validated_parameters.get('MFR'),
            'hfr': validated_parameters.get('HFR')
        })
        
        response = AnalysisResponse(
            result_id=result_id,
            parameters=blood_params,
            disease_predictions=disease_list,
            severity_level=severity_level,
            risk_score=risk_score,
            recommendations=recommendations,
            normal_ranges=NORMAL_RANGES
        )
        
        logger.info(f"Analysis completed successfully for result ID: {result_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

def _determine_disease_severity(disease_name: str, probability: float, parameters: Dict[str, float]) -> str:
    """Determine severity for a specific disease"""
    if probability > 0.8:
        return 'high'
    elif probability > 0.5:
        return 'medium'
    else:
        return 'low'

def _get_confidence_level(probability: float) -> str:
    """Get confidence level based on probability"""
    if probability > 0.8:
        return "High"
    elif probability > 0.6:
        return "Medium"
    else:
        return "Low"

def _calculate_risk_score(disease_predictions: List[Dict], parameters: Dict[str, float]) -> float:
    """Calculate overall risk score"""
    if not disease_predictions:
        return 0.0
    
    # Use highest probability as base risk score
    max_prob = max(disease['probability'] for disease in disease_predictions)
    
    # Adjust based on number of abnormal parameters
    abnormal_count = sum(1 for param, value in parameters.items() 
                        if _is_abnormal_parameter(param, value))
    abnormality_factor = min(1.0, abnormal_count / 10)
    
    return min(1.0, max_prob + (abnormality_factor * 0.2))

def _determine_severity(risk_score: float) -> str:
    """Determine severity level based on risk score"""
    if risk_score >= 0.8:
        return "Critical"
    elif risk_score >= 0.6:
        return "High Risk"
    elif risk_score >= 0.4:
        return "Medium Risk"
    elif risk_score >= 0.2:
        return "Low Risk"
    else:
        return "Normal"

def _is_abnormal_parameter(param: str, value: float) -> bool:
    """Check if parameter value is abnormal"""
    if param in NORMAL_RANGES:
        normal_min = NORMAL_RANGES[param]['min']
        normal_max = NORMAL_RANGES[param]['max']
        return value < normal_min or value > normal_max
    return False

@router.get("/history", response_model=List[AnalysisResult])
async def get_analysis_history(current_user: User = Depends(get_current_user)):
    """Get analysis history for current user"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("""
                    SELECT ar.* FROM analysis_results ar
                    JOIN patients p ON ar.patient_id = p.patient_id
                    WHERE p.user_id = :user_id
                    ORDER BY ar.analysis_date DESC
                """),
                {"user_id": current_user.user_id}
            )
            history = result.fetchall()
        
        analysis_results = []
        for row in history:
            analysis_results.append(AnalysisResult(
                result_id=row[0],
                patient_id=row[1],
                analysis_date=row[2],
                wbc=row[3],
                rbc=row[4],
                hgb=row[5],
                hct=row[6],
                mcv=row[7],
                mch=row[8],
                mchc=row[9],
                plt=row[10],
                rdw_sd=row[11],
                rdw_cv=row[12],
                pdw=row[13],
                mpv=row[14],
                p_lcr=row[15],
                pct=row[16],
                neut=row[17],
                lymph=row[18],
                mono=row[19],
                eo=row[20],
                baso=row[21],
                ig=row[22],
                nrbcs=row[23],
                reticulocytes=row[24],
                irf=row[25],
                lfr=row[26],
                mfr=row[27],
                hfr=row[28],
                severity_level=row[29],
                risk_score=row[30],
                raw_text=row[31]
            ))
        
        return analysis_results
    except Exception as e:
        logger.error(f"Get analysis history error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analysis history")

@router.get("/results/{result_id}", response_model=AnalysisResult)
async def get_analysis_result(result_id: int, current_user: User = Depends(get_current_user)):
    """Get specific analysis result"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("""
                    SELECT ar.* FROM analysis_results ar
                    JOIN patients p ON ar.patient_id = p.patient_id
                    WHERE ar.result_id = :result_id AND p.user_id = :user_id
                """),
                {"result_id": result_id, "user_id": current_user.user_id}
            )
            result_data = result.fetchone()
        
        if not result_data:
            raise HTTPException(status_code=404, detail="Analysis result not found")
        
        return AnalysisResult(
            result_id=result_data[0],
            patient_id=result_data[1],
            analysis_date=result_data[2],
            wbc=result_data[3],
            rbc=result_data[4],
            hgb=result_data[5],
            hct=result_data[6],
            mcv=result_data[7],
            mch=result_data[8],
            mchc=result_data[9],
            plt=result_data[10],
            rdw_sd=result_data[11],
            rdw_cv=result_data[12],
            pdw=result_data[13],
            mpv=result_data[14],
            p_lcr=result_data[15],
            pct=result_data[16],
            neut=result_data[17],
            lymph=result_data[18],
            mono=result_data[19],
            eo=result_data[20],
            baso=result_data[21],
            ig=result_data[22],
            nrbcs=result_data[23],
            reticulocytes=result_data[24],
            irf=result_data[25],
            lfr=result_data[26],
            mfr=result_data[27],
            hfr=result_data[28],
            severity_level=result_data[29],
            risk_score=result_data[30],
            raw_text=result_data[31]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get analysis result error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch analysis result")