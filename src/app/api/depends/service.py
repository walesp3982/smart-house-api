from typing import Annotated

from fastapi import Depends

from app.api.depends.database import (
    AreaRepositoryDep,
    DeviceRepositoryDep,
    HouserRepositoryDep,
    InstalledDeviceRepositoryDep,
    TrackDeviceRepositoryDep,
    UserRepositoryDep,
)
from app.infraestructure.speech.protocol import SpeechRecognizerProtocol
from app.infraestructure.speech.whisper import FasterWhisperRecognizer
from app.services import (
    AreaService,
    DeviceService,
    HouseService,
    InstalledDeviceService,
    TokenJWTService,
    TrackDeviceService,
    UserService,
)
from app.services.command_device import CommandDeviceService
from app.services.ollama import ChatConversationService
from app.services.status_device import StateDeviceService
from app.services.voice_text import VoiceToTextService

from .mqtt import MQTTProviderDep

TokenJWTServiceDep = Annotated[TokenJWTService, Depends()]


def get_user_service(
    user_repository: UserRepositoryDep,
) -> UserService:
    return UserService(user_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_device_service(
    device_repository: DeviceRepositoryDep,
) -> DeviceService:
    return DeviceService(device_repository)


DeviceServiceDep = Annotated[DeviceService, Depends(get_device_service)]


def get_house_service(house_repository: HouserRepositoryDep) -> HouseService:
    return HouseService(house_repository)


HouseServiceDep = Annotated[HouseService, Depends(get_house_service)]


def get_area_service(area_repository: AreaRepositoryDep) -> AreaService:
    return AreaService(area_repository)


AreaServiceDep = Annotated[AreaService, Depends(get_area_service)]


def get_installed_device_service(
    installed_device_repository: InstalledDeviceRepositoryDep,
    device_repository: DeviceRepositoryDep,
) -> InstalledDeviceService:
    return InstalledDeviceService(installed_device_repository, device_repository)


InstalledDeviceServiceDep = Annotated[
    InstalledDeviceService, Depends(get_installed_device_service)
]


def get_track_device_service(
    track_device_repository: TrackDeviceRepositoryDep,
) -> TrackDeviceService:
    return TrackDeviceService(track_device_repository)


TrackDeviceServiceDep = Annotated[TrackDeviceService, Depends(get_track_device_service)]


def get_command_device_service(
    installed_device_service: InstalledDeviceServiceDep,
    mqtt_provider: MQTTProviderDep,
    track_service: TrackDeviceServiceDep,
):
    return CommandDeviceService(installed_device_service, mqtt_provider, track_service)


CommandDeviceServiceDep = Annotated[
    CommandDeviceService, Depends(get_command_device_service)
]


def get_state_device_service(
    installed_device_service: InstalledDeviceServiceDep,
    mqtt_provider: MQTTProviderDep,
):
    return StateDeviceService(installed_device_service, mqtt_provider)


StateDeviceServiceDep = Annotated[
    StateDeviceService,
    Depends(get_state_device_service),
]


def get_ollama_service(
    installed_device_service: InstalledDeviceServiceDep,
    state_device_service: StateDeviceServiceDep,
    command_device_service: CommandDeviceServiceDep,
    track_device_service: TrackDeviceServiceDep,
    mqtt_provider: MQTTProviderDep,
) -> ChatConversationService:
    return ChatConversationService(
        installed_device_service=installed_device_service,
        track_device_service=track_device_service,
        mqtt_provider=mqtt_provider,
    )


OllamaConversationServiceDep = Annotated[
    ChatConversationService,
    Depends(get_ollama_service),
]


def get_speech_recognizer_protocol() -> SpeechRecognizerProtocol:
    return FasterWhisperRecognizer()


SpeechRecognizerProtocolDep = Annotated[
    SpeechRecognizerProtocol, Depends(get_speech_recognizer_protocol)
]


def get_voice_to_text_service(speech_recognized: SpeechRecognizerProtocolDep):
    return VoiceToTextService(speech_recognized)


VoiceToTextServiceDep = Annotated[
    VoiceToTextService,
    Depends(get_voice_to_text_service),
]
