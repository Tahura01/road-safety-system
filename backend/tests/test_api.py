import os
import sys

# Ensure pytest can find the 'app' folder natively
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient

# Must set the database securely before importing the app to avoid corrupting prod
os.environ["DATABASE_URL"] = "sqlite:///./test_sql_app.db"

from app.main import app

client = TestClient(app)

def test_read_main():
    """Test if the root API endpoint is alive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Road Safety System API"}

def test_get_dashboard_stats():
    """Test if the Dashboard statistics aggregate correctly."""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "accident_trends" in data
    assert "safety_tips" in data
    assert isinstance(data["accident_trends"], list)

def test_predict_accident_severity():
    """
    Test the AI Model prediction endpoint natively.
    Ensures Geocoding, Traffic, Weather, and ML pipeline are 
    all integrated without crashing.
    """
    payload = {"location_name": "Ahmedabad"}
    response = client.post("/api/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["location"] == "Ahmedabad"
    assert "coordinates" in data
    assert "severity_prediction" in data
    assert "dynamic_risk_score" in data
    assert isinstance(data["alerts"], list)

def test_get_hotspots():
    """Test spatial clustering endpoints."""
    response = client.get("/api/hotspots")
    assert response.status_code == 200
    data = response.json()
    # It might be empty if the mock DB was just initialized, but should be a dictionary containing structures
    assert isinstance(data, dict)
