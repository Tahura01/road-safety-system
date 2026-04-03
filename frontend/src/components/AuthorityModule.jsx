import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldAlert, MapPin, Calendar, CheckSquare } from 'lucide-react';

import { API_BASE } from '../config';

export default function AuthorityModule() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/reports`);
      setReports(res.data.reverse()); // latest first
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-700/50">
        <ShieldAlert size={32} className="text-warning" />
        <div>
          <h2 className="text-2xl font-bold text-gray-100">Authority Control Center</h2>
          <p className="text-sm text-gray-400">Review public road condition reports to inform traffic planning and improvements.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {reports.length === 0 ? (
          <div className="col-span-full py-12 text-center text-gray-500">
            No public reports submitted yet.
          </div>
        ) : (
          reports.map(report => (
            <div key={report.id} className="bg-gray-800/40 border border-gray-700/50 rounded-xl p-5 hover:bg-gray-800/60 transition">
              <div className="flex justify-between items-start mb-3">
                <span className="px-2.5 py-1 bg-red-500/10 text-red-400 rounded-md text-xs font-semibold border border-red-500/20 truncate max-w-[150px]">
                  {report.issue_type}
                </span>
                <span className="text-xs text-gray-500 flex items-center gap-1">
                  <Calendar size={12} />
                  {new Date(report.reported_at).toLocaleDateString()}
                </span>
              </div>
              
              <div className="flex items-center gap-2 text-gray-300 font-medium mb-2">
                <MapPin size={16} className="text-primary" />
                <span className="truncate">{report.location_name}</span>
              </div>
              
              <p className="text-sm text-gray-400 mb-4 line-clamp-3 h-[60px]">
                "{report.description}"
              </p>
              
              <div className="flex justify-end pt-3 border-t border-gray-700/30">
                <button className="text-xs flex items-center gap-1 text-secondary hover:text-green-400 transition">
                  <CheckSquare size={14} /> Mark Addressed
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
