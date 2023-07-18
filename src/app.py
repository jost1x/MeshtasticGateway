from service import ServiceGateway
from config import Settings
from rich import print
from database.influxdb import InfluxDB
import logging


logging.info("Cargando variables de entorno...")
settings = Settings(_env_file='dev.env') # type: ignore

influx_conf = settings.influxdb

influx = InfluxDB(influx_conf.url, influx_conf.token,
                  influx_conf.org, influx_conf.bucket, settings.influx)

service = ServiceGateway(settings.serial, influx)

try:
    service.connect()
    service.loop()
except Exception as e:
    print(e)

