import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

from app.services.geocoder_service import get_lat_lng
from app.services.weather_service import get_current_weather
from app.services.traffic_service import get_real_time_traffic
from app.ml.severity_model import predict_severity, print_model_accuracy
from app.ml.risk_model import calculate_dynamic_risk
from app.ml.spatial_clustering import get_hotspots
from datetime import datetime

import sys

try:
    models.Base.metadata.create_all(bind=engine)

    # On server startup, evaluate and print the AI project accuracy
    print_model_accuracy()
except Exception as e:
    print(f"CRITICAL STARTUP ERROR: {e}")
    sys.exit(1)

app = FastAPI(title="Road Safety System API")

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:5173",
    os.getenv("FRONTEND_URL", "https://your-vercel-app-url.vercel.app")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Road Safety System API"}

@app.post("/api/predict")
def predict_accident_details(request: schemas.PredictRequest):
    # 1. Geocode
    lat, lng = get_lat_lng(request.location_name)
    
    # 2. Get Time
    now = datetime.now()
    time_of_day = now.hour
    
    # 3. Get Weather
    weather = get_current_weather(lat, lng)
    
    # 4. Get Traffic
    traffic_index = get_real_time_traffic(lat, lng, time_of_day)
    
    # 5. Predict Severity (Mocking road_type as Urban for simplicity)
    severity = predict_severity(time_of_day, weather, traffic_index, "Urban", use_xgboost=True)
    
    # 6. Predict Risk
    risk_prob, risk_score = calculate_dynamic_risk(time_of_day, weather, traffic_index)
    
    # 7. Generate Alerts
    alerts = []
    if risk_score > 70:
        alerts.append(f"High accident risk zone ({weather} / Traffic: {traffic_index}/10)")
        alerts.append("Drive slow - accident hotspot area.")
    elif risk_score > 40:
        alerts.append(f"Moderate conditions. Weather: {weather}.")
    
    alerts.append("Safety: Wear helmets for 2 wheeler and seat belts for 4 wheeler.")
        
    return {
        "location": request.location_name,
        "coordinates": {"lat": lat, "lng": lng},
        "weather": weather,
        "traffic_index": traffic_index,
        "time_of_day": time_of_day,
        "severity_prediction": severity,
        "risk_level": risk_prob,
        "dynamic_risk_score": risk_score,
        "alerts": alerts
    }

@app.get("/api/hotspots")
def get_map_hotspots():
    # Returns clusters and heatmaps generated from the mock dataset
    return get_hotspots()

@app.post("/api/reports", response_model=schemas.ReportOut)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    if report.latitude is None or report.longitude is None:
        lat, lng = get_lat_lng(report.location_name)
        report.latitude = lat
        report.longitude = lng
        
    db_report = models.UserReport(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/api/reports", response_model=list[schemas.ReportOut])
def get_reports(db: Session = Depends(get_db)):
    return db.query(models.UserReport).all()

@app.get("/api/dashboard")
def get_dashboard_stats():
    return {
        "accident_trends": [
            {"month": "Jan", "count": 40},
            {"month": "Feb", "count": 30},
            {"month": "Mar", "count": 25},
            {"month": "Apr", "count": 15}
        ],
        "high_risk_timings": ["18:00 - 20:00", "08:00 - 10:00"],
        "past_month_percentage": -15, # 15% decrease
        "safety_tips": [
            "Maintain safe distance",
            "Avoid driving during heavy rain",
            "Obey speed limits"
        ]
    }
