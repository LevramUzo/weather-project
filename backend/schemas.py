from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class WeatherCreate(BaseModel):
    location: str
    date_from: str
    date_to: str

    @validator('date_to')
    def validate_dates(cls, date_to, values):
        try:
            start = datetime.strptime(values['date_from'], "%Y-%m-%d")
            end = datetime.strptime(date_to, "%Y-%m-%d")
            if end < start:
                raise ValueError("date_to must be after date_from")
        except ValueError as e:
            raise ValueError(str(e))
        return date_to

class WeatherUpdate(BaseModel):
    location: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None

class WeatherResponse(BaseModel):
    id: int
    location: str
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    date_from: str
    date_to: str
    temperature_celsius: Optional[float]
    humidity: Optional[float]
    wind_kph: Optional[float]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
