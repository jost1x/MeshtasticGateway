from service import ServiceGateway
from config import Settings
from rich import print
from database.influxdb import InfluxDB
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Cargando variables de entorno...")
settings = Settings(_env_file="dev.env")  # type: ignore

influx_conf = settings.influxdb

influx: InfluxDB = InfluxDB(
    influx_conf.url,
    influx_conf.token,
    influx_conf.org,
    influx_conf.bucket,
    settings.enable_influx,
)

service = ServiceGateway(settings.serial, influx)

try:
    service.connect()
    service.loop()
except Exception as e:
    logging.exception(str(e))  # Log the exception with traceback