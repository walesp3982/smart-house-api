from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, device, house, user, voice
from app.settings import general_settings

app = FastAPI()

origins = list(general_settings.cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(house.router)
app.include_router(voice.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
