from pydantic import BaseModel
from datetime import datetime


class Position(BaseModel):
    time: datetime
    latitude: float | None = None
    longitude: float | None = None
    altitude: int | None = None
    altitudeHae: int | None = None
    satsInView: int | None

    class Config:
        json_encoders = {datetime: lambda v: datetime.fromtimestamp(v)}


class User(BaseModel):
    id: str
    longName: str
    shortName: str
    macaddr: str
    hwModel: str


class TextMessage(BaseModel):
    pass


class DeviceMetrics(BaseModel):
    batteryLevel: int | None = None
    voltage: float | None = None
    airUtilTx: float | None  = None 
    channelUtilization: float | None

class Telemetry(BaseModel):
    time: datetime
    deviceMetrics: DeviceMetrics | None

    class Config:
        json_encoders = {datetime: lambda v: datetime.fromtimestamp(v)}

