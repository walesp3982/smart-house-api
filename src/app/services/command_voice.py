# voice/service.py
import httpx

from app.entities import DeviceEntity
from app.infraestructure.speech.protocol import SpeechRecognizerProtocol
from app.settings import general_settings


class CommandVoiceService:
    def __init__(
        self,
        recognizer: SpeechRecognizerProtocol,
        devices: list[DeviceEntity],
        house_id: int,
    ):
        self._recognizer = recognizer
        self._devices = devices
        self._base_url = general_settings.app_host
        self._house_id = house_id

    def process(self, wav_bytes: bytes) -> dict:
        text = self._recognizer.transcribe(wav_bytes)
        action = self._match_action(text)
        device = self._match_device(text)

        if not action or not device:
            return {"transcription": text, "action": "unknown"}

        url = f"{self._base_url}/houses/{self._house_id}/devices/{device.id}/query"
        response = httpx.post(url, params={"action": action})
        return {
            "transcription": text,
            "action": action,
            "status": response.status_code,
        }

    def _match_action(self, text: str) -> str | None:
        text = text.lower()
        for device in self._devices:
            for command in device.type.command():
                for action in command.actions:
                    if action in text:
                        return command.naming_broker
        return None

    def _match_device(self, text: str):
        text = text.lower()
        for device in self._devices:
            # Todo: Corregir esto
            return device
        return None
