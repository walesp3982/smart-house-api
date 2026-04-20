from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.depends.mqtt import init_mqtt_provider
from app.api.routes import (
    area,
    auth,
    chat,
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
    init_mqtt_provider()

    yield
    MQTTClient.disconnect()


app = FastAPI(lifespan=lifespan)

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
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
