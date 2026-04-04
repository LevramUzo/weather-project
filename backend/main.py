from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, WeatherRecord
from schemas import WeatherCreate, WeatherUpdate, WeatherResponse
from typing import List
import crud
import export
import requests

# ─── App Setup ───────────────────────────────────────────
app = FastAPI(
    title="Weather App API",
    description="""
    ## Weather App — PM Accelerator Technical Assessment
    
    Built by: Opara Marvellous Uzoma
    
    About PM Accelerator:
    PM Accelerator is the #1 product manager community in the world. 
    Our mission is to empower aspiring and experienced product managers 
    with the tools, mentorship, and real-world experience needed to 
    accelerate their careers in product management.
    
    🌐 www.pmaccelerator.io
    """,
    version="1.0.0"
)

# ─── Database Setup ───────────────────────────────────────
DATABASE_URL = "sqlite:///./weather.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# ─── API Keys ─────────────────────────────────────────────
YOUTUBE_API_KEY = "insert_youtube_api_key_here"
OPENWEATHER_API_KEY = os.env("WEATHER_API_KEY","497bfb602e130d355959e7fb8662c589")

# ─── Dependency ───────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── CRUD ENDPOINTS ───────────────────────────────────────

# CREATE
@app.post("/weather", response_model=WeatherResponse)
def create_weather(weather: WeatherCreate, db: Session = Depends(get_db)):
    record = crud.create_weather_record(db, weather)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Location '{weather.location}' not found. Please enter a valid city."
        )
    return record

# READ ALL
@app.get("/weather", response_model=List[WeatherResponse])
def get_all_weather(db: Session = Depends(get_db)):
    records = crud.get_all_records(db)
    if not records:
        raise HTTPException(status_code=404, detail="No records found in database")
    return records

# READ ONE
@app.get("/weather/{record_id}", response_model=WeatherResponse)
def get_one_weather(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return record

# UPDATE
@app.put("/weather/{record_id}", response_model=WeatherResponse)
def update_weather(record_id: int, updated: WeatherUpdate, db: Session = Depends(get_db)):
    record = crud.update_weather_record(db, record_id, updated)
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Record {record_id} not found or location invalid"
        )
    return record

# DELETE
@app.delete("/weather/{record_id}")
def delete_weather(record_id: int, db: Session = Depends(get_db)):
    record = crud.delete_weather_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return {"message": f"Record {record_id} deleted successfully"}

# ─── EXPORT ENDPOINTS ─────────────────────────────────────

@app.get("/export")
def export_data(format: str = "json", db: Session = Depends(get_db)):
    records = crud.get_all_records(db)
    if not records:
        raise HTTPException(status_code=404, detail="No records to export")

    if format == "csv":
        return PlainTextResponse(export.export_csv(records), media_type="text/csv")
    elif format == "json":
        return PlainTextResponse(export.export_json(records), media_type="application/json")
    elif format == "xml":
        return PlainTextResponse(export.export_xml(records), media_type="application/xml")
    elif format == "markdown":
        return PlainTextResponse(export.export_markdown(records), media_type="text/markdown")
    elif format == "pdf":
        return Response(export.export_pdf(records), media_type="application/pdf")
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Choose: json, csv, xml, markdown, pdf")

# ─── BONUS API ENDPOINTS ──────────────────────────────────

# YouTube Videos of location
@app.get("/youtube/{record_id}")
def get_youtube_videos(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "q": f"{record.location} {record.country} travel",
        "key": YOUTUBE_API_KEY,
        "part": "snippet",
        "maxResults": 5,
        "type": "video"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="YouTube API error")
    
    data = response.json()
    videos = []
    for item in data.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        })
    return {"location": record.location, "videos": videos}

# Google Maps data of location
@app.get("/map/{record_id}")
def get_map_data(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {
        "location": record.location,
        "country": record.country,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "google_maps_url": f"https://www.google.com/maps?q={record.latitude},{record.longitude}",
        "embed_url": f"https://maps.google.com/maps?q={record.latitude},{record.longitude}&output=embed"
    }