import requests
import logging
from urllib.parse import quote

def get_lat_lng(location_name: str):
    """
    Open-Meteo Geocoding API.
    Works best with native city strings. Do not append long suffix strings.
    """
    query = location_name.strip()
        
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(query)}&count=1&language=en&format=json"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return float(result['latitude']), float(result['longitude'])
    except Exception as e:
        logging.error(f"Geocoding error: {e}")
        
    # Fallback to Gandhinagar, Gujarat center
    return 23.2156, 72.6369
