# speech/protocol.py
from typing import Protocol, runtime_checkable


@runtime_checkable
class SpeechRecognizerProtocol(Protocol):
    """
    Protocolo para transcribir wav a texto
    """

    def transcribe(self, wav_bytes: bytes, suffix: str = ".wav") -> str: ...
