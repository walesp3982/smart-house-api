import io

import speech_recognition as sr
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/voice", tags=["voz"])


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".wav", ".flac", ".aiff")):
        raise HTTPException(
            status_code=400,
            detail="Formato de audio no soportado. Usa WAV, FLAC o AIFF.",
        )

    recognizer = sr.Recognizer()
    audio_bytes = await file.read()

    try:
        audio = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="es-ES")
        return {"transcription": text}
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="No se pudo reconocer el audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el audio: {e}")
