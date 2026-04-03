import React, { useState } from 'react';
import axios from 'axios';
import { Search, Loader2, AlertTriangle, ShieldAlert } from 'lucide-react';

import { API_BASE } from '../config';

const getRiskColor = (level) => {
  if (level === 'High Risk') return 'text-danger bg-danger/10 border-danger/20';
  if (level === 'Medium Risk') return 'text-warning bg-warning/10 border-warning/20';
  return 'text-secondary bg-secondary/10 border-secondary/20';
};

export default function PredictionPanel({ onLocationFound }) {
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!location) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/api/predict`, { location_name: location });
      setData(response.data);
      if (response.data.coordinates && onLocationFound) {
        onLocationFound(response.data.coordinates);
      }
    } catch (error) {
      console.error("Prediction error", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-200">Trip AI Prediction</h2>
      
      <form onSubmit={handlePredict} className="relative mb-6">
        <input 
          type="text" 
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter destination (e.g., Ahmedabad)" 
          className="w-full bg-gray-800/50 border border-gray-700/50 rounded-xl py-3 pl-4 pr-12 focus:outline-none focus:ring-2 focus:ring-primary transition"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="absolute right-2 top-2 p-1.5 bg-primary hover:bg-blue-600 rounded-lg transition disabled:opacity-50"
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Search size={18} />}
        </button>
      </form>

      {data && (
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className={`p-4 rounded-xl border flex flex-col gap-2 ${getRiskColor(data.risk_level)}`}>
            <div className="flex justify-between items-center">
              <span className="font-medium">Risk Probability</span>
              <span className="font-bold text-lg">{data.risk_level}</span>
            </div>
            <div className="flex justify-between items-center text-sm opacity-80">
              <span>Dynamic Risk Score</span>
              <span>{data.dynamic_risk_score}/100</span>
            </div>
            <div className="w-full bg-black/20 rounded-full h-1.5 mt-2">
              <div 
                className={`h-1.5 rounded-full ${data.risk_level.includes('High') ? 'bg-danger' : data.risk_level.includes('Medium') ? 'bg-warning' : 'bg-secondary'}`} 
                style={{ width: `${data.dynamic_risk_score}%` }}
              ></div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="bg-gray-800/40 p-3 rounded-xl border border-gray-700/30">
              <p className="text-xs text-gray-400 mb-1">Predicted Severity</p>
              <p className="font-semibold text-gray-200">{data.severity_prediction}</p>
            </div>
            <div className="bg-gray-800/40 p-3 rounded-xl border border-gray-700/30">
              <p className="text-xs text-gray-400 mb-1">Weather Context</p>
              <p className="font-semibold text-gray-200">{data.weather}</p>
            </div>
          </div>

          <div className="bg-orange-500/10 border border-orange-500/20 p-4 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-orange-400 mb-2">
              <AlertTriangle size={18} />
              <h3 className="font-semibold text-sm">System Alerts</h3>
            </div>
            <ul className="text-sm space-y-1 text-gray-300">
              {data.alerts.map((alert, idx) => (
                <li key={idx} className="flex gap-2 items-start">
                  <span className="text-orange-500 mt-0.5">•</span>
                  <span>{alert}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!data && !loading && (
        <div className="flex flex-col items-center justify-center py-8 text-gray-500 gap-3">
          <ShieldAlert size={48} className="opacity-20" />
          <p className="text-sm text-center">Enter a location to predict accident risk, severity, and get AI alerts.</p>
        </div>
      )}
    </div>
  );
}
