import random

def get_real_time_traffic(lat: float, lng: float, time_of_day: int):
    """
    Mocking traffic explicitly optimized for Indian metropolises.
    Since no unauthenticated free real-time traffic API exists, this simulates TomTom's flow 
    focusing on Indian peak hours (9AM-11AM structure & 6PM-9PM).
    """
    base_traffic = 4 # Average chaotic traffic floor in Indian metros
    
    # Morning rush (9, 10) and Evening rush (18, 19, 20)
    if time_of_day in [9, 10, 18, 19, 20]:
        base_traffic = 9 
    elif time_of_day in [8, 11, 17, 21]:
        base_traffic = 6
        
    fluctuation = random.randint(-1, 2)
    traffic_index = base_traffic + fluctuation
    
    return max(1, min(traffic_index, 10))
