import requests
import logging

def get_current_weather(lat: float, lng: float):
    """
    Fetches real-time weather from Open-Meteo API.
    Returns categorized strings matching our trained AI model: 'Clear', 'Rain', 'Fog', 'Cloudy'.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            wmo_code = data.get("current_weather", {}).get("weathercode", 0)
            return map_wmo_to_condition(wmo_code)
    except Exception as e:
        logging.error(f"Failed to fetch real weather from Open-Meteo: {e}")
    
    return "Clear"

def map_wmo_to_condition(code: int) -> str:
    # Detailed WMO codes: https://open-meteo.com/en/docs
    if code in [0, 1]: 
        return "Clear"
    elif code in [2, 3]: 
        return "Cloudy"
    elif code in [45, 48]: 
        return "Fog"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]: 
        return "Rain"
    elif code in [71, 73, 75, 85, 86]: 
        return "Rain" # Treating snow slightly as rain/bad conditions if applicable in North India
    return "Clear"
