# voice/service.py
from app.entities.installed_device import InstalledDeviceWithDevice
from app.exceptions.device_exception import ActionDeviceNotFound
from app.exceptions.installed_device import InstalledDeviceNotFound
from app.infraestructure.speech.protocol import SpeechRecognizerProtocol
from app.settings import general_settings


class CommandVoiceService:
    def __init__(
        self,
        recognizer: SpeechRecognizerProtocol,
        devices: list[InstalledDeviceWithDevice],
        house_id: int,
    ):
        self._recognizer = recognizer
        self._devices = devices
        self._base_url = general_settings.app_host
        self._house_id = house_id

    def process(self, wav_bytes: bytes) -> dict:
        ## Procesa el audio
        text = self._recognizer.transcribe(wav_bytes)

        installed_device = self.get_device(text)
        if installed_device is None:
            raise InstalledDeviceNotFound
        action = self.get_action(text, installed_device)

        if action is None:
            raise ActionDeviceNotFound

        return {
            "installed_devices_id": installed_device.id,
            "transcription": text,
            "action": action,
        }

    def get_action(
        self,
        text: str,
        installed_device: InstalledDeviceWithDevice,
    ) -> str | None:
        text = text.lower()
        for command in installed_device.device.type.command():
            for action in command.actions:
                if action in text:
                    return command.naming_broker
        return None

    def get_device(self, text: str) -> InstalledDeviceWithDevice | None:
        """
        Obtenemos el InstalledDeviceEntity por su nombre
        """
        text = text.lower()
        for device in self._devices:
            if device.name in text:
                return device
        return None
