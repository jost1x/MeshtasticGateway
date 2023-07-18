from pydantic import BaseModel
from datetime import datetime
from models.decoded_message import Position, User, Telemetry


class Decoded(BaseModel):
    portnum: str
    payload: bytes
    position: Position | None
    user: User | None
    text: str | None
    telemetry: Telemetry | None


class BasePacket(BaseModel):
    decoded: Decoded
    rxTime: datetime | None
    rxSnr: float | None
    fromId: str | None
    toId: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: datetime.fromtimestamp(v)
        }
