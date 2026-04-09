import io

import speech_recognition as sr
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.schemas.general import ErrorResponse
from app.api.schemas.voice import TranscribeResponse

router = APIRouter(prefix="/voice", tags=["voz"])


def parse_command(text: str):
    text = text.lower()
    if "enciende" in text or "encender" in text:
        return {"action": "turn_on", "device": "light", "message": "Encendiendo la luz"}
    elif "apaga" in text or "apagar" in text:
        return {"action": "turn_off", "device": "light", "message": "Apagando la luz"}
    else:
        return {"action": "unknown", "message": "Comando no reconocido"}


@router.post(
    "/transcribe",
    responses={
        200: {
            "description": "Transcripción y comando procesado exitosamente",
        },
        400: {
            "model": ErrorResponse,
            "description": "Archivo no válido o audio no reconocido",
        },
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
)
async def transcribe_audio(file: UploadFile = File(...)) -> TranscribeResponse:

    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se subió ningún archivo",
        )
    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400, detail="Formato de audio no soportado. Usa WAV."
        )

    recognizer = sr.Recognizer()
    audio_bytes = await file.read()

    try:
        audio = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="es-ES")  # type: ignore
        command = parse_command(text)
        return TranscribeResponse(
            transcription=text,
            action=command["action"],
            device=command.get("device"),
            message=command["message"],
        )
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="No se pudo reconocer el audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el audio: {e}")
