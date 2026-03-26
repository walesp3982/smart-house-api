import io

import speech_recognition as sr


class GoogleSpeechRecognizer:
    def __init__(self, language: str = "es-ES"):
        self._recognizer = sr.Recognizer()
        self._language = language

    def transcribe(self, wav_bytes: bytes) -> str:
        audio_file = sr.AudioFile(io.BytesIO(wav_bytes))
        with audio_file as source:
            audio_data = self._recognizer.record(source)
        return self._recognizer.recognize_google(audio_data, language=self._language)  # type: ignore
