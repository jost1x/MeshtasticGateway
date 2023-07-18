from pydantic import BaseSettings, BaseModel


class InfluxDBModel(BaseModel):
    bucket: str
    org: str
    token: str
    url: str


class Settings(BaseSettings):
    serial: str = '/dev/ttyACM0'
    influx: bool = False
    influxdb: InfluxDBModel


    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
