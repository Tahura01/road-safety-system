import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import axios from 'axios';
import { TrendingDown, Clock, ShieldCheck } from 'lucide-react';

import { API_BASE } from '../config';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get(`${API_BASE}/api/dashboard`).then(res => setStats(res.data)).catch(console.error);
  }, []);

  if (!stats) return <div className="p-8 text-center text-gray-400">Loading metrics...</div>;

  return (
    <div className="space-y-6">
      {/* Top Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 flex flex-col gap-2">
          <div className="text-secondary mb-2"><TrendingDown size={28} /></div>
          <h3 className="text-gray-400 text-sm">Monthly Accident Rate</h3>
          <p className="text-3xl font-bold">{stats.past_month_percentage}%</p>
          <p className="text-xs text-secondary">Improvement from last month</p>
        </div>
        
        <div className="glass-panel p-6 flex flex-col gap-2">
          <div className="text-warning mb-2"><Clock size={28} /></div>
          <h3 className="text-gray-400 text-sm">High-Risk Timings</h3>
          <div className="flex flex-wrap gap-2 mt-1">
            {stats.high_risk_timings.map(t => (
              <span key={t} className="px-3 py-1 bg-warning/10 text-warning rounded-full text-xs border border-warning/20">
                {t}
              </span>
            ))}
          </div>
        </div>

        <div className="glass-panel p-6 flex flex-col gap-2">
          <div className="text-primary mb-2"><ShieldCheck size={28} /></div>
          <h3 className="text-gray-400 text-sm">AI Safety Advisories</h3>
          <ul className="text-xs space-y-2 mt-1 text-gray-300">
            {stats.safety_tips.map((tip, i) => (
              <li key={i} className="flex gap-2"><span className="text-primary">•</span>{tip}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Charts */}
      <div className="glass-panel p-6 h-[400px]">
        <h3 className="text-lg font-semibold mb-6">Accident Trends (Past Months)</h3>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={stats.accident_trends}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
            <XAxis dataKey="month" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <RechartsTooltip 
              contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '8px' }}
              itemStyle={{ color: '#E5E7EB' }}
            />
            <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
