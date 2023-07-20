from pydantic import ValidationError
from meshtastic.serial_interface import SerialInterface
from pubsub import pub
from rich import print
from time import sleep

from database.influxdb import InfluxDB
from models.base import BasePacket
from protocol.position_app import PositionApp
from protocol.telemetry import TelemetryApp


class ServiceGateway:
    serial: str
    interface: SerialInterface
    influx: InfluxDB | None = None

    def __init__(
        self, serial: str = "/dev/ttyACM0", influx: InfluxDB | None = None
    ) -> None:
        self.serial = serial
        self.influx = influx
        self.subscriptions()

    def subscriptions(self) -> None:
        pub.subscribe(self.onReceive, "meshtastic.receive")

    def connect(self):
        self.interface = SerialInterface(devPath=self.serial)

    def loop(self):
        while True:
            sleep(0.1)

    def onReceive(self, packet, interface):
        try:
            message = BasePacket.parse_obj(packet)
            self.protocol_matching(message=message)
        except ValidationError as e:
            print(e.json())

    def protocol_matching(self, message: BasePacket) -> None:
        protocol_handlers = {
            "ADMIN_APP": self.handle_admin_app,
            "TEXT_MESSAGE_APP": self.handle_text_message_app,
            "POSITION_APP": self.handle_position_app,
            "NODEINFO_APP": self.handle_nodeinfo_app,
            "TELEMETRY_APP": self.handle_telemetry_app,
        }
        portnum = message.decoded.portnum
        handler = protocol_handlers.get(portnum, self.handle_unknown_protocol)
        handler(message)

    def handle_admin_app(self, message: BasePacket):
        print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")

    def handle_text_message_app(self, message: BasePacket):
        print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")

    def handle_position_app(self, message: BasePacket):
        protocol = PositionApp(message)
        protocol.save_data(self.influx)

    def handle_nodeinfo_app(self, message: BasePacket):
        print(f"NOT_IMPLEMENTED: {message.decoded.portnum}")

    def handle_telemetry_app(self, message: BasePacket):
        protocol = TelemetryApp(message)
        protocol.save_data(self.influx)

    def handle_unknown_protocol(self, message: BasePacket):
        print(f"NOT_REGISTER_PROTOCOL: {message.decoded.portnum}")
