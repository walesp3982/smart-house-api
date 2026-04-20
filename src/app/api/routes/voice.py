import speech_recognition as sr
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.depends.service import VoiceToTextServiceDep
from app.api.schemas.general import ErrorResponse
from app.api.schemas.voice import TranscribeResponse

router = APIRouter(prefix="/voice", tags=["voz"])


@router.post(
    "/transcribe",
    responses={
        200: {
            "description": "Transcripción de audio a texto",
        },
        400: {
            "model": ErrorResponse,
            "description": "Archivo no válido o audio no reconocido",
        },
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
)
async def transcribe_audio(
    voice_to_text_service: VoiceToTextServiceDep,
    file: UploadFile = File(...),
) -> TranscribeResponse:

    if file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se subió ningún archivo",
        )
    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400, detail="Formato de audio no soportado. Usa WAV."
        )

    audio_bytes = await file.read()

    try:
        text = voice_to_text_service.process(audio_bytes)
        return TranscribeResponse(transcription=text)
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="No se pudo reconocer el audio")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el audio: {e}")
