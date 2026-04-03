import pandas as pd
import numpy as np
import random
import os

def generate_mock_historical_data(num_samples=2500):
    np.random.seed(42)
    random.seed(42)
    
    # Key Gujarat urban centers
    hotspot_centers = [
        {"lat": 23.0225, "lng": 72.5714, "city": "Ahmedabad"},
        {"lat": 21.1702, "lng": 72.8311, "city": "Surat"},
        {"lat": 22.3072, "lng": 73.1812, "city": "Vadodara"},
        {"lat": 22.3039, "lng": 70.8022, "city": "Rajkot"},
        {"lat": 21.7645, "lng": 72.1519, "city": "Bhavnagar"},
    ]
    
    lats = []
    lngs = []
    for _ in range(num_samples):
        center = random.choice(hotspot_centers)
        # Random dispersion ~10-15km radius
        lat_offset = np.random.normal(0, 0.05) 
        lng_offset = np.random.normal(0, 0.05)
        lats.append(center["lat"] + lat_offset)
        lngs.append(center["lng"] + lng_offset)
        
    weather_conditions = ['Clear', 'Rain', 'Fog', 'Cloudy'] # Simplified mapping
    road_types = ['Highway', 'Urban', 'Rural', 'Arterial']
    
    data = {
        'latitude': lats,
        'longitude': lngs,
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
    
    def calc_risk(row):
        score = 0
        if row['weather'] != 'Clear': score += 1
        if row['traffic_index'] > 6: score += 1
        
        if score >= 2: return 'High'
        elif score == 1: return 'Medium'
        else: return 'Low'
        
    df['risk_probability'] = df.apply(calc_risk, axis=1)
    
    return df

if __name__ == "__main__":
    df = generate_mock_historical_data()
    # Use absolute path for safety during imports from different dirs
    path = os.path.join(os.path.dirname(__file__), "..", "..", "historical_accidents.csv")
    df.to_csv(path, index=False)
    print("Generated Indian mock dataset: historical_accidents.csv")
