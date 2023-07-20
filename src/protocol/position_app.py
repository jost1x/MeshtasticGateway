from database.influxdb import InfluxDB
from models.base import BasePacket
from models.decoded_message import Position
from database.influxdb import Point

class PositionApp:
    packet: BasePacket

    def __init__(self, packet: BasePacket) -> None:
        self.packet = packet

    def save_data(self, influx: InfluxDB | None):
        position: Position | None = self.packet.decoded.position

        if position is not None:
            fields: dict[str, float | int | None] = {
                "latitude": position.latitude,
                "longitude": position.longitude,
                "altitude": position.altitude,
                "altitudeHae": position.altitudeHae,
                "satsInView": position.satsInView,
            }

            point = (
                Point("tbeam")
                .tag("device", self.packet.fromId)
                .time(position.time)
            )

            for k, v in fields.items():
                if v is not None:
                    point.field(k, v)

            if influx is not None:
                influx.write(point)
