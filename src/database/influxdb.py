from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteApi
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDB:

    client: InfluxDBClient
    write_api: WriteApi
    org: str
    enabled: bool = True

    def __init__(self, url: str, token: str, org: str , bucket: str, enabled: bool) -> None:
        self.client = InfluxDBClient(url=url, token=token, org=org) 
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.org = org
        self.bucket = bucket
        self.enabled = enabled


    def write(self, point: Point): 
        if self.enabled:
            self.write_api.write(self.bucket, self.org, point)
