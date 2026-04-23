from app.infraestructure.speech.protocol import SpeechRecognizerProtocol


class VoiceToTextService:
    def __init__(
        self,
        recognizer: SpeechRecognizerProtocol,
    ):
        self._recognizer = recognizer

    def process(self, wav_bytes: bytes, suffix: str) -> str:
        ## Procesa el audio
        text = self._recognizer.transcribe(wav_bytes, suffix=suffix)

        return text
