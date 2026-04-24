# import io
import os
import tempfile

from faster_whisper import WhisperModel


class FasterWhisperRecognizer:
    def __init__(self, model_size: str = "small", language: str = "es"):
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self._language = language

    def transcribe(self, wav_bytes: bytes, suffix: str = ".wav") -> str:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(wav_bytes)
            tmp_path = f.name
        try:
            segments, _ = self._model.transcribe(tmp_path, language=self._language)
            return " ".join(s.text for s in segments).strip()
        finally:
            os.unlink(tmp_path)
