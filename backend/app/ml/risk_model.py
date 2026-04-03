def calculate_dynamic_risk(time_of_day, weather, traffic_index):
    # Dynamic Risk Score 0-100
    base_score = 10
    
    # Time factor
    if time_of_day >= 22 or time_of_day <= 5: 
        base_score += 25  # Night time
    elif time_of_day >= 17 and time_of_day <= 20:
        base_score += 20  # Evening rush
        
    # Weather factor
    weather_risks = {
        'Clear': 0,
        'Cloudy': 10,
        'Rain': 25,
        'Fog': 30,
        'Snow': 35
    }
    base_score += weather_risks.get(weather, 15)
    
    # Traffic factor (assuming 1-10 scale)
    base_score += (traffic_index * 3) # Up to 30
    
    # Normalize
    final_score = min(score_clamp(base_score), 100)
    
    # Category
    if final_score < 40:
        probability = "Low Risk"
    elif final_score < 70:
        probability = "Medium Risk"
    else:
        probability = "High Risk"
        
    return probability, final_score

def score_clamp(score):
    return max(0, score)
