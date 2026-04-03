import React, { useState } from 'react';
import PredictionPanel from './components/PredictionPanel';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';
import ReportIssueForm from './components/ReportIssueForm';
import AuthorityModule from './components/AuthorityModule';
import { ShieldCheck, Map as MapIcon, BarChart3, AlertTriangle, ShieldAlert } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('user'); // 'user', 'dashboard', 'authority'
  const [searchedLocation, setSearchedLocation] = useState(null);
  return (
    <div className="min-h-screen p-6 relative overflow-hidden">
      {/* Background Decoratives */}
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary/20 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-secondary/20 rounded-full blur-3xl pointer-events-none"></div>

      <header className="max-w-7xl mx-auto flex justify-between items-center mb-8 relative z-10 glass-panel p-4">
        <div className="flex items-center gap-3 text-primary z-10">
          <ShieldCheck size={36} />
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            Road Safety AI
          </h1>
        </div>
        <nav className="flex gap-4">
          <button 
            onClick={() => setActiveTab('user')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl transition ${activeTab === 'user' ? 'bg-primary/20 text-primary border border-primary/50' : 'hover:bg-gray-800'}`}
          >
            <MapIcon size={20} /> Driver View
          </button>
          <button 
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl transition ${activeTab === 'dashboard' ? 'bg-secondary/20 text-secondary border border-secondary/50' : 'hover:bg-gray-800'}`}
          >
            <BarChart3 size={20} /> Global Analytics
          </button>
          <button 
            onClick={() => setActiveTab('authority')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl transition ${activeTab === 'authority' ? 'bg-warning/20 text-warning border border-warning/50' : 'hover:bg-gray-800'}`}
          >
            <ShieldAlert size={20} /> Authority Module
          </button>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto relative z-10">
        {activeTab === 'user' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1 space-y-6">
              <PredictionPanel onLocationFound={setSearchedLocation} />
              <ReportIssueForm />
            </div>
            <div className="lg:col-span-2 h-[600px] glass-panel p-4 flex flex-col">
              <h2 className="text-xl font-semibold mb-4 text-gray-200">Live Safety Map</h2>
              <div className="flex-1 rounded-xl overflow-hidden shadow-inner border border-gray-700/50">
                <MapView searchedLocation={searchedLocation} />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'authority' && <AuthorityModule />}
      </main>
    </div>
  );
}

export default App;
