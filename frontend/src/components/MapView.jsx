import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';

import { API_BASE } from '../config';

function LocationUpdater({ location }) {
  const map = useMap();
  useEffect(() => {
    if (location && location.lat && location.lng) {
      map.flyTo([location.lat, location.lng], 12, { duration: 1.5 });
    }
  }, [location, map]);
  return null;
}

export default function MapView({ searchedLocation }) {
  const [hotspots, setHotspots] = useState({ clusters: [], kmeans_centers: [], dbscan_clusters: [], heatmap_points: [] });

  useEffect(() => {
    axios.get(`${API_BASE}/api/hotspots?t=${new Date().getTime()}`)
      .then(res => setHotspots(res.data))
      .catch(console.error);
  }, []);

  return (
    <MapContainer center={[22.2587, 71.1924]} zoom={7} style={{ height: '100%', minHeight: '500px', width: '100%', background: '#0B0F19' }}>
      <LocationUpdater location={searchedLocation} />
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
      />
      
      {/* KMeans Macro Zones */}
      {hotspots.kmeans_centers?.map((center, idx) => (
        <CircleMarker
          key={`kmeans-${idx}`}
          center={[center.lat, center.lng]}
          radius={40}
          pathOptions={{ color: '#3B82F6', fillColor: '#3B82F6', fillOpacity: 0.1, weight: 1 }}
        >
          <Tooltip>Macro Risk Zone (KMeans)</Tooltip>
        </CircleMarker>
      ))}

      {/* DBSCAN Micro Hotspots */}
      {hotspots.dbscan_clusters?.map((cluster, idx) => (
        <CircleMarker
          key={`dbscan-${idx}`}
          center={[cluster.lat, cluster.lng]}
          radius={Math.min(cluster.intensity * 2 + 5, 25)}
          pathOptions={{ color: '#EF4444', fillColor: '#EF4444', fillOpacity: 0.5, weight: 2 }}
        >
          <Tooltip>Micro Hotspot (Identified events: {cluster.intensity})</Tooltip>
        </CircleMarker>
      ))}

      {/* Simulated Heatmap Points as small intense markers */}
      {hotspots.heatmap_points?.map((pt, idx) => (
        <CircleMarker
          key={`heat-${idx}`}
          center={[pt.lat, pt.lng]}
          radius={pt.intensity * 1.5}
          pathOptions={{ 
            color: pt.intensity === 5.0 ? '#EF4444' : '#F59E0B', 
            fillOpacity: 0.6, 
            stroke: false 
          }}
        />
      ))}
    </MapContainer>
  );
}
