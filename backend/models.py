
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date_from = Column(String, nullable=False)
    date_to = Column(String, nullable=False)
    temperature_celsius = Column(Float)
    humidity = Column(Float)
    wind_kph = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)