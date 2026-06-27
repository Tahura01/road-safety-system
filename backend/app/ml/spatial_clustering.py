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
            
            # Find the most common city and area if the columns exist
            cluster_city = cluster_points['city'].mode()[0] if 'city' in cluster_points.columns else "Unknown"
            cluster_area = cluster_points['area'].mode()[0] if 'area' in cluster_points.columns else "Location"
            
            # Find average or mode for risk
            predominant_severity = cluster_points['severity'].mode()[0] if 'severity' in cluster_points.columns else "Minor"
            predominant_risk = cluster_points['risk_probability'].mode()[0] if 'risk_probability' in cluster_points.columns else "Low"
            avg_risk_score = round(cluster_points['risk_score'].mean(), 1) if 'risk_score' in cluster_points.columns else 0

            hotspots_response["dbscan_clusters"].append({
                "lat": center_lat,
                "lng": center_lng,
                "city": cluster_city,
                "area": cluster_area,
                "severity": predominant_severity,
                "risk_level": predominant_risk,
                "risk_score": avg_risk_score,
                "intensity": len(cluster_points),
                "type": "Micro Hotspot"
            })
            
    # Heatmap points (all points)
    for _, row in df.iterrows():
        intensity = 1.0
        if row.get('severity') == "Fatal":
            intensity = 5.0
        elif row.get('severity') == "Serious":
            intensity = 3.0
            
        hotspots_response["heatmap_points"].append({
            "lat": row['latitude'],
            "lng": row['longitude'],
            "intensity": intensity
        })

    return hotspots_response
