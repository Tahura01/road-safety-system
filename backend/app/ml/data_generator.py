import pandas as pd
import numpy as np
import random
import os

def generate_mock_historical_data(num_samples=2500):
    np.random.seed(42)
    random.seed(42)
    
    # Key Gujarat urban centers with specific areas and highways
    hotspot_centers = [
        # Ahmedabad
        {"lat": 23.0450, "lng": 72.5080, "city": "Ahmedabad", "area": "SG Highway"},
        {"lat": 23.0330, "lng": 72.5690, "city": "Ahmedabad", "area": "Ashram Road"},
        {"lat": 23.0640, "lng": 72.5180, "city": "Ahmedabad", "area": "SP Ring Road"},
        # Surat
        {"lat": 21.1440, "lng": 72.7660, "city": "Surat", "area": "Dumas Road"},
        {"lat": 21.1960, "lng": 72.8360, "city": "Surat", "area": "Ring Road"},
        # Vadodara
        {"lat": 22.3360, "lng": 73.2000, "city": "Vadodara", "area": "NH48 Highway"},
        {"lat": 22.3210, "lng": 73.1550, "city": "Vadodara", "area": "Gotri Road"},
        {"lat": 22.2590, "lng": 73.1950, "city": "Vadodara", "area": "Makarpura Road"},
        {"lat": 22.3730, "lng": 73.1670, "city": "Vadodara", "area": "NE1 Expressway"},
        # Rajkot
        {"lat": 22.2610, "lng": 70.8040, "city": "Rajkot", "area": "Gondal Road"},
        {"lat": 22.2850, "lng": 70.7810, "city": "Rajkot", "area": "150 Feet Ring Road"},
        # Bhavnagar
        {"lat": 21.7580, "lng": 72.1380, "city": "Bhavnagar", "area": "Waghawadi Road"},
        # Halol
        {"lat": 22.5020, "lng": 73.4730, "city": "Halol", "area": "Halol-Vadodara Toll Road"},
        {"lat": 22.4800, "lng": 73.4800, "city": "Halol", "area": "Halol GIDC"}
    ]
    
    lats, lngs, cities, areas = [], [], [], []
    for _ in range(num_samples):
        center = random.choice(hotspot_centers)
        # Tighter random dispersion (~2-5km radius) to reflect the specific highway/area
        lat_offset = np.random.normal(0, 0.015) 
        lng_offset = np.random.normal(0, 0.015)
        lats.append(center["lat"] + lat_offset)
        lngs.append(center["lng"] + lng_offset)
        cities.append(center["city"])
        areas.append(center["area"])
        
    weather_conditions = ['Clear', 'Rain', 'Fog', 'Cloudy']
    road_types = ['Highway', 'Urban', 'Rural', 'Arterial']
    
    data = {
        'latitude': lats,
        'longitude': lngs,
        'city': cities,
        'area': areas,
        'time_of_day': np.random.randint(0, 24, num_samples), 
        'weather': np.random.choice(weather_conditions, num_samples, p=[0.5, 0.25, 0.1, 0.15]),
        'traffic_index': np.random.randint(1, 10, num_samples), 
        'road_type': np.random.choice(road_types, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    def calc_severity(row):
        score = 0
        if row['weather'] in ['Rain', 'Fog']: score += 2
        if row['traffic_index'] > 6: score += 1
        if row['time_of_day'] < 6 or row['time_of_day'] > 20: score += 1
        
        # Introduce randomness (15% chance of severe deviation from logic) to simulate human unpredictability
        fuzz = random.random()
        if fuzz < 0.05:
            return 'Fatal' # 5% unexpected fatal
        elif fuzz < 0.15:
            return 'Minor' # 10% miraculously minor despite conditions
            
        if score >= 3: return 'Fatal'
        elif score == 2: return 'Serious'
        else: return 'Minor'
        
    df['severity'] = df.apply(calc_severity, axis=1)
    
    from app.ml.risk_model import calculate_dynamic_risk
    
    def apply_risk(row):
        prob, score = calculate_dynamic_risk(row['time_of_day'], row['weather'], row['traffic_index'])
        return pd.Series([prob, score])
        
    df[['risk_probability', 'risk_score']] = df.apply(apply_risk, axis=1)
    
    return df

if __name__ == "__main__":
    df = generate_mock_historical_data()
    # Use absolute path for safety during imports from different dirs
    path = os.path.join(os.path.dirname(__file__), "..", "..", "historical_accidents.csv")
    df.to_csv(path, index=False)
    print("Generated Indian mock dataset: historical_accidents.csv")
