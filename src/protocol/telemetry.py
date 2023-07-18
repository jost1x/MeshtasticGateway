from database.influxdb import InfluxDB, Point
from models.base import BasePacket, Telemetry
from rich import print


class TelemetryApp:

    packet: BasePacket
    influx: InfluxDB | None

    def __init__(self, packet: BasePacket, influx: InfluxDB | None ) -> None:
        self.packet = packet
        self.influx = influx

    def save_data(self):
        if self.influx is not None:
            telemetry: Telemetry | None = self.packet.decoded.telemetry

            if telemetry is not None:
                if telemetry.deviceMetrics is not None:
                    fields = {
                        'batteryLevel': telemetry.deviceMetrics.batteryLevel,
                        'voltage': telemetry.deviceMetrics.voltage,
                        'airUtilTx': telemetry.deviceMetrics.airUtilTx,
                    }

                    point = Point('tbeam').tag('device', self.packet.fromId)
        
                    for k, v in fields.items():
                        if v is not None:
                            point = point.field(k, v)

                    point = point.time(telemetry.time)
        
                    self.influx.write(point)