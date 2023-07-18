from database.influxdb import InfluxDB
from models.base import BasePacket
from database.influxdb import InfluxDB, Point
from models.decoded_message import Position

class PositionApp:

    packet: BasePacket
    influx: InfluxDB | None

    def __init__(self, packet: BasePacket, influx: InfluxDB | None) -> None:
        self.packet = packet
        self.influx = influx

    def save_data(self):
        if self.influx is not None:
            position: Position | None = self.packet.decoded.position

            if position is not None:

                fields = {
                    'latitude': position.latitude,
                    'longitude': position.longitude,
                    'altitude': position.altitude,
                    'altitudeHae': position.altitudeHae,
                    'satsInView': position.satsInView
                }

       
                point = Point('tbeam').tag('device', self.packet.fromId)

                for k, v in fields.items():
                    if v is not None:
                        point = point.field(k, v)

                point = point.time(position.time)
                
                self.influx.write(point)
