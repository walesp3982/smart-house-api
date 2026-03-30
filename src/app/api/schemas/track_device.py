from datetime import datetime

from pydantic import BaseModel


class TrackDeviceResponse(BaseModel):
    id: int
    device_id: int
    status: str
    timestamp: datetime
