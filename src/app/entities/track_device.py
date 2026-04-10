from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class StatusDevice(StrEnum):
    ON = "on"
    OFF = "off"


class TrackDevice(BaseModel):
    id: int | None = None
    device_id: int
    status: StatusDevice
    timestamp: datetime
