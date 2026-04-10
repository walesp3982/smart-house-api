import io

from pydub import AudioSegment


class ConverterService:
    def to_wav(self, audio_bytes: bytes) -> bytes:
        """
        Convertir el formato web a formato .wav
        """
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        buf = io.BytesIO()
        audio.export(buf, format="wav", parameters=["-ar", "16000", "-ac", "1"])
        return buf.getvalue()
