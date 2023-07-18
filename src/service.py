from pydantic import ValidationError
from meshtastic.serial_interface import SerialInterface
from pubsub import pub
from rich import print

from database.influxdb import InfluxDB, Point
from models.base import BasePacket
from protocol import PositionApp
from protocol.telemetry import TelemetryApp

ALLOW_PROTOCOL = [
    "TEXT_MESSAGE_APP",
    "POSITION_APP",
    "NODEINFO_APP",
    "TELEMETRY_APP"
]

NOT_IMPLEMENTED = None


class ServiceGateway:

    serial: str
    interface: SerialInterface
    influx: InfluxDB | None = None

    def __init__(self, serial: str = '/dev/ttyACM0', influx: InfluxDB | None = None) -> None:
        self.serial = serial
        self.influx = influx
        self.subscriptions()

    def subscriptions(self) -> None:
        pub.subscribe(self.onReceive, "meshtastic.receive")

    def connect(self):
        self.interface = SerialInterface(devPath=self.serial)

    def loop(self):
        while True:
            pass

    def onReceive(self, packet, interface):
        try: 
            message = BasePacket.parse_obj(packet)
            self.protocol_matching(message=message)
        except ValidationError as e:
            print(e.json())

    def protocol_matching(self, message: BasePacket):
        match message.decoded.portnum:
            case "ADMIN_APP":
                print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")
            case "TEXT_MESSAGE_APP":
                print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")
            case "POSITION_APP":
                protocol = PositionApp(message, self.influx)
                protocol.save_data()
            case "NODEINFO_APP":
                print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")
            case "TELEMETRY_APP":
                protocol = TelemetryApp(message, self.influx)
                protocol.save_data()
            case _:
                print(f"NOT_REGISTER_PROTOCOL: {message.decoded.portnum}")
