from database.influxdb import InfluxDB, Point
from models.base import BasePacket
from models.decoded_message import Telemetry

class TelemetryApp:
    packet: BasePacket

    def __init__(self, packet: BasePacket) -> None:
        self.packet = packet

    def save_data(self, influx: InfluxDB | None):
        telemetry: Telemetry | None = self.packet.decoded.telemetry

        if telemetry is not None and telemetry.deviceMetrics is not None:
            fields: dict[str, float | int | None] = {
                'batteryLevel': telemetry.deviceMetrics.batteryLevel,
                'voltage': telemetry.deviceMetrics.voltage,
                'airUtilTx': telemetry.deviceMetrics.airUtilTx,
            }

            point = (
                Point('tbeam')
                .tag('device', self.packet.fromId)
                .time(telemetry.time)
            )

            for k, v in fields.items():
                if v is not None:
                    point.field(k, v)

            if influx is not None:
                influx.write(point)