
from sqlalchemy.orm import Session
from models import WeatherRecord
from schemas import WeatherCreate, WeatherUpdate
import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "f3fd0fbfdb8e6b912a8fe44ed6d8f96f")

def get_weather_from_api(location: str):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    print("API Response:", data)  # for debugging
    
    if response.status_code != 200:
        return None
    
    return {
        "location": data.get("name", location),
        "country": data.get("sys", {}).get("country", "Unknown"),
        "latitude": data.get("coord", {}).get("lat", 0),
        "longitude": data.get("coord", {}).get("lon", 0),
        "temperature_celsius": data.get("main", {}).get("temp", 0),
        "humidity": data.get("main", {}).get("humidity", 0),
        "wind_kph": data.get("wind", {}).get("speed", 0) * 3.6,
        "description": data.get("weather", [{}])[0].get("description", "N/A")
    }

# CREATE
def create_weather_record(db: Session, weather: WeatherCreate):
    api_data = get_weather_from_api(weather.location)
    
    if not api_data:
        return None  # location doesn't exist
    
    db_record = WeatherRecord(
        location=api_data["location"],
        country=api_data["country"],
        latitude=api_data["latitude"],
        longitude=api_data["longitude"],
        date_from=weather.date_from,
        date_to=weather.date_to,
        temperature_celsius=api_data["temperature_celsius"],
        humidity=api_data["humidity"],
        wind_kph=api_data["wind_kph"],
        description=api_data["description"]
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# READ ALL
def get_all_records(db: Session):
    return db.query(WeatherRecord).all()

# READ ONE
def get_record_by_id(db: Session, record_id: int):
    return db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()

# UPDATE
def update_weather_record(db: Session, record_id: int, updated_data: WeatherUpdate):
    record = get_record_by_id(db, record_id)
    if not record:
        return None
    
    if updated_data.location:
        api_data = get_weather_from_api(updated_data.location)
        if not api_data:
            return None
        record.location = api_data["location"]
        record.country = api_data["country"]
        record.latitude = api_data["latitude"]
        record.longitude = api_data["longitude"]
        record.temperature_celsius = api_data["temperature_celsius"]
        record.humidity = api_data["humidity"]
        record.wind_kph = api_data["wind_kph"]
        record.description = api_data["description"]
    
    if updated_data.date_from:
        record.date_from = updated_data.date_from
    if updated_data.date_to:
        record.date_to = updated_data.date_to
    
    db.commit()
    db.refresh(record)
    return record

# DELETE
def delete_weather_record(db: Session, record_id: int):
    record = get_record_by_id(db, record_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record