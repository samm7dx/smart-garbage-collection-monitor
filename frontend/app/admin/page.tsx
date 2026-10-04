'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { getBins, getAnalytics, getComplaints, updateComplaintStatus, recordCollection, predictRisk, type AnalyticsSummary, type Bin, type Complaint } from '@/lib/api';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { Trash2, AlertTriangle, CheckCircle2, Clock, MapPin, Activity } from 'lucide-react';

const Map = dynamic(() => import('@/components/ui/Map'), { ssr: false });

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [bins, setBins] = useState<Bin[]>([]);
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [predictionMessage, setPredictionMessage] = useState('');

  const fetchData = async () => {
    try {
      setError('');
      const [anData, binsData, compData] = await Promise.all([
        getAnalytics(),
        getBins(),
        getComplaints()
      ]);
      setAnalytics(anData);
      setBins(binsData);
      setComplaints(compData);
    } catch {
      setError('Failed to load dashboard data. Please check backend/API configuration.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void fetchData();
  }, []);

  const handlePredict = async (id: number) => {
    try {
      const res = await predictRisk(id);
      setPredictionMessage(`Bin ${res.bin_id}: Risk level is ${res.risk_level} (Prob: ${res.risk_probability})`);
      await fetchData();
    } catch {
      alert("Error predicting risk.");
    }
  };

  const handleRecordCollection = async (binId: number) => {
    try {
      await recordCollection(binId);
      await fetchData();
    } catch {
      alert("Error recording collection.");
    }
  };

  const handleResolveComplaint = async (id: number) => {
    try {
      await updateComplaintStatus(id, 'RESOLVED');
      await fetchData();
    } catch {
      alert("Error updating complaint.");
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-500 font-medium">Loading dashboard...</div>;
  if (error) return <div className="p-8 text-center text-red-600 font-medium">{error}</div>;
  if (!analytics) return <div className="p-8 text-center text-slate-500 font-medium">No dashboard data available.</div>;

  const notifications: string[] = [];
  const highRiskBins = bins.filter(b => b.status === 'OVERFLOW_RISK');
  if (highRiskBins.length > 0) {
    notifications.push(`${highRiskBins.length} bins have a high predicted overflow risk.`);
  }
  const missedBins = bins.filter(b => b.status === 'MISSED');
  if (missedBins.length > 0) {
    notifications.push(`${missedBins.length} bins missed their collection schedule.`);
  }
  const openComps = complaints.filter(c => c.status === 'OPEN');
  if (openComps.length > 0) {
    notifications.push(`There are ${openComps.length} open complaints from residents.`);
  }

  const pieData = [
    { name: 'On-Time', value: analytics.on_time_collections, color: '#10b981' },
    { name: 'Delayed', value: analytics.delayed_collections, color: '#f59e0b' },
    { name: 'Missed', value: analytics.missed_collections, color: '#ef4444' }
  ].filter(d => d.value > 0);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Admin Dashboard</h1>
          <p className="text-slate-500">System overview and analytics</p>
        </div>
      </div>

      {notifications.length > 0 && (
        <div className="bg-orange-50 border-l-4 border-orange-500 p-4 rounded-r-lg shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-orange-600" />
            <h3 className="font-bold text-orange-800">System Notifications</h3>
          </div>
          <ul className="list-disc list-inside text-sm text-orange-700 space-y-1 ml-1">
            {notifications.map((n, i) => <li key={i}>{n}</li>)}
          </ul>
        </div>
      )}

      {predictionMessage && (
        <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg flex items-center justify-between shadow-sm">
          <span className="text-blue-800 font-medium">{predictionMessage}</span>
          <button onClick={() => setPredictionMessage('')} className="text-blue-500 font-bold hover:text-blue-700 bg-blue-100 rounded-full w-6 h-6 flex items-center justify-center pb-1">×</button>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <KPICard title="Total Bins" value={analytics.total_bins} icon={Trash2} color="text-blue-600" bg="bg-blue-50" />
        <KPICard title="On-Time" value={analytics.on_time_collections} icon={CheckCircle2} color="text-green-600" bg="bg-green-50" />
        <KPICard title="Delayed" value={analytics.delayed_collections} icon={Clock} color="text-orange-600" bg="bg-orange-50" />
        <KPICard title="Missed" value={analytics.missed_collections} icon={AlertTriangle} color="text-red-600" bg="bg-red-50" />
        <KPICard title="High Risk" value={analytics.high_risk_bins} icon={Activity} color="text-purple-600" bg="bg-purple-50" />
        <KPICard title="Complaints" value={analytics.open_complaints} icon={MapPin} color="text-pink-600" bg="bg-pink-50" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 min-h-[400px] flex flex-col">
          <h2 className="text-lg font-bold mb-4 text-slate-800">Live Map</h2>
          <div className="flex-1 min-h-[350px]">
            {bins.length > 0 ? (
             <Map bins={bins} onPredict={handlePredict} />
            ) : (
             <div className="h-full flex items-center justify-center text-slate-500">No bins available to display on the map.</div>
            )}
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
          <h2 className="text-lg font-bold mb-4 text-slate-800">Collection Status</h2>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={70} outerRadius={110} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="p-6 border-b border-slate-100">
            <h2 className="text-lg font-bold text-slate-800">Bin Status List</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-600 font-semibold">
                <tr>
                  <th className="p-4 whitespace-nowrap">Bin</th>
                  <th className="p-4 whitespace-nowrap">Area</th>
                  <th className="p-4 whitespace-nowrap">Fill %</th>
                  <th className="p-4 whitespace-nowrap">Status</th>
                  <th className="p-4 whitespace-nowrap">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {bins.length === 0 ? (
                  <tr>
                    <td className="p-4 text-slate-500" colSpan={5}>No bin records available.</td>
                  </tr>
                ) : bins.map(b => (
                  <tr key={b.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4 font-medium text-slate-700">{b.name}</td>
                    <td className="p-4 text-slate-600">{b.area}</td>
                    <td className="p-4">
                      <span className={`font-bold ${b.current_fill_percentage > 80 ? 'text-red-600' : 'text-slate-700'}`}>
                        {b.current_fill_percentage.toFixed(0)}%
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${b.status === 'NORMAL' ? 'bg-green-100 text-green-700' : b.status === 'OVERFLOW_RISK' ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700'}`}>
                        {b.status}
                      </span>
                    </td>
                    <td className="p-4">
                      <button onClick={() => handleRecordCollection(b.id)} className="text-blue-600 font-medium hover:text-blue-800 transition-colors bg-blue-50 px-3 py-1 rounded hover:bg-blue-100">
                        Collect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col max-h-[600px]">
          <div className="p-6 border-b border-slate-100 shrink-0">
            <h2 className="text-lg font-bold text-slate-800">Recent Complaints</h2>
          </div>
          <div className="divide-y divide-slate-100 overflow-y-auto">
            {complaints.length === 0 ? (
              <p className="p-6 text-slate-500">No complaints reported.</p>
            ) : (
              complaints.map(c => (
                <div key={c.id} className="p-6 hover:bg-slate-50 flex justify-between items-start gap-4 transition-colors">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-bold text-slate-800">Bin {c.bin_id} ({c.area})</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-bold ${c.status === 'OPEN' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                        {c.status}
                      </span>
                    </div>
                    <p className="text-sm text-slate-600">{c.description}</p>
                    <p className="text-xs text-slate-400 mt-2">{new Date(c.reported_at).toLocaleString()}</p>
                  </div>
                  {c.status === 'OPEN' && (
                    <button onClick={() => handleResolveComplaint(c.id)} className="px-3 py-1.5 bg-green-50 text-green-700 font-medium text-sm rounded hover:bg-green-100 transition-colors">
                      Resolve
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({
  title,
  value,
  icon: Icon,
  color,
  bg
}: {
  title: string;
  value: number;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  bg: string;
}) {
  return (
    <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-sm font-medium text-slate-500">{title}</h3>
        <div className={`p-2 rounded-lg ${bg} ${color}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <p className="text-3xl font-extrabold text-slate-800">{value}</p>
    </div>
  );
}
