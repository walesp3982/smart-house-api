import json
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.depends.mqtt import get_mqtt_provider
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


# -------------------------------
# NUEVA RUTA /ask con Ollama
# -------------------------------


class AskRequest(BaseModel):
    question: str


def llamar_a_ollama(prompt: str) -> str:
    resultado = subprocess.run(
        ["ollama", "run", "llama2", "--prompt", prompt], capture_output=True, text=True
    )
    return resultado.stdout.strip()


@app.post("/ask")
async def ask(request: AskRequest):
    question = request.question

    prompt = f"""
    Responde SOLO con un JSON válido.
    No escribas texto adicional.
    Formato esperado:
    {{"action": "state_device"}}
    o
    {{"action": "execute_command"}}
    El usuario preguntó: "{question}".
    """

    respuesta = llamar_a_ollama(prompt)

    # Para depuración, devolvemos la respuesta cruda de Ollama
    return {"ollama_raw": respuesta}
