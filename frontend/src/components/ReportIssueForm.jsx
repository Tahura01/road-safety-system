import React, { useState } from 'react';
import axios from 'axios';
import { AlertCircle, CheckCircle2, Send } from 'lucide-react';

import { API_BASE } from '../config';

export default function ReportIssueForm() {
  const [formData, setFormData] = useState({
    location_name: '',
    issue_type: 'Pothole',
    description: ''
  });
  const [status, setStatus] = useState('idle'); // idle, submitting, success, error

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.location_name || !formData.description) return;

    setStatus('submitting');
    try {
      await axios.post(`${API_BASE}/api/reports`, formData);
      setStatus('success');
      setFormData({ location_name: '', issue_type: 'Pothole', description: '' });
      setTimeout(() => setStatus('idle'), 3000);
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center gap-2 mb-4">
        <AlertCircle className="text-warning" size={24} />
        <h2 className="text-xl font-semibold text-gray-200">Report Road Condition</h2>
      </div>
      
      <p className="text-sm text-gray-400 mb-4">Help us map hazards by reporting potholes, broken signals, or poor lighting.</p>
      
      {status === 'success' ? (
        <div className="bg-secondary/10 border border-secondary/20 p-4 rounded-xl flex items-center gap-3 text-secondary animate-in fade-in zoom-in duration-300">
          <CheckCircle2 />
          <p className="text-sm font-medium">Report submitted successfully! Thank you.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs text-gray-400 mb-1 ml-1 cursor-pointer">Location</label>
            <input 
              type="text" 
              required
              value={formData.location_name}
              onChange={(e) => setFormData({...formData, location_name: e.target.value})}
              placeholder="e.g., enter street name or landmark" 
              className="w-full bg-gray-800/50 border border-gray-700/50 rounded-xl py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary transition text-sm"
            />
          </div>
          
          <div>
            <label className="block text-xs text-gray-400 mb-1 ml-1 cursor-pointer">Issue Type</label>
            <select 
              value={formData.issue_type}
              onChange={(e) => setFormData({...formData, issue_type: e.target.value})}
              className="w-full bg-gray-800/50 border border-gray-700/50 rounded-xl py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary transition text-sm text-gray-200"
            >
              <option value="Pothole">Pothole</option>
              <option value="Broken Signal">Broken Signal</option>
              <option value="Poor Lighting">Poor Lighting</option>
              <option value="Faded Lane Markings">Faded Lane Markings</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-xs text-gray-400 mb-1 ml-1 cursor-pointer">Description</label>
            <textarea 
              required
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Provide brief details..." 
              rows={3}
              className="w-full bg-gray-800/50 border border-gray-700/50 rounded-xl py-2 px-3 focus:outline-none focus:ring-2 focus:ring-primary transition text-sm resize-none"
            />
          </div>

          <button 
            type="submit" 
            disabled={status === 'submitting'}
            className="w-full bg-gray-700 hover:bg-gray-600 text-gray-100 font-medium py-2 rounded-xl transition flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {status === 'submitting' ? 'Submitting...' : (
              <>Submit Report <Send size={16} /></>
            )}
          </button>
        </form>
      )}
    </div>
  );
}
