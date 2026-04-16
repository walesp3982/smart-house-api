import json
import subprocess
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.depends.auth import PayloadDep, get_user_current
from app.api.depends.mqtt import get_mqtt_provider
from app.api.depends.service import OllamaConversationServiceDep
from app.api.routes import (
    area,
    auth,
    device,
    house,
    installed_device,
    track_device,
    user,
    voice,
    websocket,
)
from app.entities import UserEntity
from app.infraestructure.mqtt.client import MQTTClient
from app.settings import general_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    MQTTClient.connect()
    get_mqtt_provider()
    yield
    MQTTClient.disconnect()


app = FastAPI()

origins = list(general_settings.cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas ya existentes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(house.router)
app.include_router(area.router)
app.include_router(installed_device.router)
app.include_router(track_device.router)
app.include_router(voice.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# =====================================
# RUTA MEJORADA /ask con Ollama
# Maneja conversaciones multi-turno
# Consulta y ejecuta órdenes en dispositivos
# =====================================


class AskRequest(BaseModel):
    """
    Solicitud para consultar o controlar dispositivos mediante Ollama
    """

    question: str


class AskResponse(BaseModel):
    """
    Respuesta del asistente inteligente
    """

    response: str
    conversation_history: list[dict[str, str]] = []


@app.post("/ask", response_model=AskResponse)
async def ask_ollama(
    request: AskRequest,
    current_user: Annotated[UserEntity, Depends(get_user_current)],
    ollama_service: OllamaConversationServiceDep,
) -> AskResponse:
    """
    Procesa preguntas y órdenes de voz mediante Ollama

    Ejemplos:
    - "¿Cuántas luces están prendidas?" → Consulta estado y responde
    - "Apaga todas las luces" → Ejecuta el comando
    - "¿Cuál es la temperatura?" → Consulta termostatos

    Args:
        request: Pregunta u orden del usuario
        current_user: Usuario autenticado
        ollama_service: Servicio de integración con Ollama

    Returns:
        AskResponse con la respuesta natural y el historial de conversación
    """
    try:
        if current_user.id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        response = ollama_service.process_message(
            user_message=request.question,
            user_id=current_user.id,
        )

        return AskResponse(
            response=response,
            conversation_history=ollama_service.get_conversation_history(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando la solicitud: {str(e)}",
        )


@app.post("/ask/reset")
async def reset_conversation(
    current_user: Annotated[UserEntity, Depends(get_user_current)],
    ollama_service: OllamaConversationServiceDep,
) -> dict:
    """
    Reinicia el historial de conversación
    """
    ollama_service.clear_history()
    return {"message": "Historial de conversación reiniciado"}
