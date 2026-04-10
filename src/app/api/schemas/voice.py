from pydantic import BaseModel


class TranscribeResponse(BaseModel):
    transcription: str
    action: str
    device: str | None = None
    message: str
