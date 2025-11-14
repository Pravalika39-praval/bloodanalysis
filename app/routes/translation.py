# backend/app/routes/translation.py
from fastapi import APIRouter, HTTPException
from app.services.translation_service import TranslationService, TextToSpeechService

router = APIRouter(prefix="/api/translate", tags=["Translation"])

translator = TranslationService()
tts = TextToSpeechService()

@router.post("/")
def translate_text(payload: dict):
    text = payload.get("text", "")
    target_lang = payload.get("lang", "en")
    translated = translator.translate_text(text, target_lang)
    return {"translated": translated}

@router.post("/speak")
def speak_text(payload: dict):
    text = payload.get("text", "")
    lang = payload.get("lang", "en")
    path = tts.generate_speech(text, lang)
    if not path:
        raise HTTPException(status_code=500, detail="Speech generation failed")
    return {"audio_url": f"/static/{path}"}
