import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import os

def get_hotspots():
    if not os.path.exists("historical_accidents.csv"):
        return {"clusters": [], "heatmaps": []}
        
    df = pd.read_csv("historical_accidents.csv")
    
    # Extract coordinates
    coords = df[['latitude', 'longitude']].values
    
    # 1. K-Means for predefined number of high-risk zones (e.g., 5 macro regions)
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['kmeans_cluster'] = kmeans.fit_predict(coords)
    
    # 2. DBSCAN for dense micro-hotspots (frequent accidents in close proximity)
    # eps is distance parameter, min_samples is minimum points to form a cluster
    # Rough approx: 0.001 degrees is ~111 meters
    dbscan = DBSCAN(eps=0.005, min_samples=10)
    df['dbscan_cluster'] = dbscan.fit_predict(coords)
    
    hotspots_response = {
        "kmeans_centers": [],
        "dbscan_clusters": [],
        "heatmap_points": []
    }
    
    # Add KMeans centers
    for center in kmeans.cluster_centers_:
        hotspots_response["kmeans_centers"].append({
            "lat": center[0],
            "lng": center[1],
            "type": "Macro Zone"
        })
        
    # Process DBSCAN clusters (ignore noise labeled as -1)
    for cluster_id in pd.Series(df['dbscan_cluster']).unique():
        if cluster_id != -1:
            cluster_points = df[df['dbscan_cluster'] == cluster_id]
            center_lat = cluster_points['latitude'].mean()
            center_lng = cluster_points['longitude'].mean()
            hotspots_response["dbscan_clusters"].append({
                "lat": center_lat,
                "lng": center_lng,
                "intensity": len(cluster_points),
                "type": "Micro Hotspot"
            })
            
    # Heatmap points (all points)
    for _, row in df.iterrows():
        intensity = 1.0
        if row['severity'] == "Fatal":
            intensity = 5.0
        elif row['severity'] == "Serious":
            intensity = 3.0
            
        hotspots_response["heatmap_points"].append({
            "lat": row['latitude'],
            "lng": row['longitude'],
            "intensity": intensity
        })

    return hotspots_response
