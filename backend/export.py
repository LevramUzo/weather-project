import csv
import json
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import StringIO, BytesIO
from models import WeatherRecord
from typing import List

# CSV Export
def export_csv(records: List[WeatherRecord]) -> str:
    output = StringIO()
    writer = csv.writer(output)
    
    # Header row
    writer.writerow([
        "ID", "Location", "Country", "Latitude", "Longitude",
        "Date From", "Date To", "Temperature (°C)", 
        "Humidity (%)", "Wind (kph)", "Description", "Created At"
    ])
    
    # Data rows
    for r in records:
        writer.writerow([
            r.id, r.location, r.country, r.latitude, r.longitude,
            r.date_from, r.date_to, r.temperature_celsius,
            r.humidity, r.wind_kph, r.description, r.created_at
        ])
    
    return output.getvalue()

# JSON Export
def export_json(records: List[WeatherRecord]) -> str:
    data = []
    for r in records:
        data.append({
            "id": r.id,
            "location": r.location,
            "country": r.country,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "date_from": r.date_from,
            "date_to": r.date_to,
            "temperature_celsius": r.temperature_celsius,
            "humidity": r.humidity,
            "wind_kph": r.wind_kph,
            "description": r.description,
            "created_at": str(r.created_at)
        })
    return json.dumps(data, indent=2)

# XML Export
def export_xml(records: List[WeatherRecord]) -> str:
    root = ET.Element("WeatherRecords")
    for r in records:
        record = ET.SubElement(root, "Record")
        ET.SubElement(record, "ID").text = str(r.id)
        ET.SubElement(record, "Location").text = r.location
        ET.SubElement(record, "Country").text = r.country
        ET.SubElement(record, "Latitude").text = str(r.latitude)
        ET.SubElement(record, "Longitude").text = str(r.longitude)
        ET.SubElement(record, "DateFrom").text = r.date_from
        ET.SubElement(record, "DateTo").text = r.date_to
        ET.SubElement(record, "Temperature").text = str(r.temperature_celsius)
        ET.SubElement(record, "Humidity").text = str(r.humidity)
        ET.SubElement(record, "Wind").text = str(r.wind_kph)
        ET.SubElement(record, "Description").text = r.description
        ET.SubElement(record, "CreatedAt").text = str(r.created_at)
    return ET.tostring(root, encoding="unicode")

# Markdown Export
def export_markdown(records: List[WeatherRecord]) -> str:
    lines = []
    lines.append("# Weather Records\n")
    lines.append("| ID | Location | Country | Date From | Date To | Temp (°C) | Humidity | Wind (kph) | Description |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in records:
        lines.append(f"| {r.id} | {r.location} | {r.country} | {r.date_from} | {r.date_to} | {r.temperature_celsius} | {r.humidity} | {r.wind_kph} | {r.description} |")
    return "\n".join(lines)

# PDF Export
def export_pdf(records: List[WeatherRecord]) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Weather Records Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "PM Accelerator Technical Assessment")
    
    y = height - 110
    for r in records:
        if y < 100:
            c.showPage()
            y = height - 50
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"{r.id}. {r.location}, {r.country}")
        y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(70, y, f"Date Range: {r.date_from} to {r.date_to}")
        y -= 15
        c.drawString(70, y, f"Temperature: {r.temperature_celsius}°C  |  Humidity: {r.humidity}%  |  Wind: {r.wind_kph} kph")
        y -= 15
        c.drawString(70, y, f"Conditions: {r.description}")
        y -= 25
    
    c.save()
    buffer.seek(0)
    return buffer.read()