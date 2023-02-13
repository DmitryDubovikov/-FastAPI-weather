from datetime import datetime
from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str


class WeatherSchema(BaseModel):
    name: str
    city_id: int
    time: datetime
    temperature: float
    pressure: int
    wind: int
