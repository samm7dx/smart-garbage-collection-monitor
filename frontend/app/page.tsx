'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { getBins, submitComplaint } from '@/lib/api';
import { AlertCircle, CheckCircle2, Clock } from 'lucide-react';

const Map = dynamic(() => import('@/components/ui/Map'), { ssr: false });

export default function ResidentPage() {
  const [bins, setBins] = useState([]);
  const [complaintArea, setComplaintArea] = useState('Koramangala');
  const [complaintDesc, setComplaintDesc] = useState('');
  const [binId, setBinId] = useState<number | ''>('');
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchBins();
  }, []);

  const fetchBins = async () => {
    try {
      const data = await getBins();
      setBins(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleComplaint = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!binId) return alert('Please select a bin ID');
    try {
      await submitComplaint({ bin_id: Number(binId), area: complaintArea, description: complaintDesc });
      setMessage('Complaint submitted successfully!');
      setComplaintDesc('');
      setBinId('');
    } catch (e) {
      setMessage('Error submitting complaint');
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="text-center space-y-4 max-w-3xl mx-auto py-12">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">
          Smart Garbage Collection
        </h1>
        <p className="text-lg text-slate-600">
          Monitoring irregular garbage collection using data analytics, GIS, and machine learning.
        </p>
        <div className="flex justify-center gap-8 pt-4">
          <div className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shadow-inner">
              <Clock className="w-6 h-6" />
            </div>
            <span className="font-semibold text-sm text-slate-700">Monitor</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 shadow-inner">
              <AlertCircle className="w-6 h-6" />
            </div>
            <span className="font-semibold text-sm text-slate-700">Predict</span>
          </div>
          <div className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 shadow-inner">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <span className="font-semibold text-sm text-slate-700">Act</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-4 rounded-2xl shadow-sm border border-slate-100 min-h-[500px] flex flex-col">
          <h2 className="text-xl font-bold mb-4 px-2 text-slate-800">Collection Points Map</h2>
          <div className="flex-1 min-h-[400px]">
            {!loading && <Map bins={bins} />}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h2 className="text-xl font-bold mb-6 text-slate-800">Report Missed Collection</h2>
          
          {message && (
            <div className="mb-6 p-4 rounded-xl bg-blue-50 text-blue-700 font-medium text-sm flex items-start gap-3 border border-blue-100">
              <CheckCircle2 className="w-5 h-5 shrink-0 text-blue-600" />
              <p>{message}</p>
            </div>
          )}

          <form onSubmit={handleComplaint} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Area</label>
              <select 
                className="w-full rounded-xl border-slate-200 shadow-sm px-4 py-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                value={complaintArea}
                onChange={(e) => setComplaintArea(e.target.value)}
              >
                <option>Koramangala</option>
                <option>Indiranagar</option>
                <option>Jayanagar</option>
                <option>Whitefield</option>
                <option>Malleswaram</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Bin ID (Check map)</label>
              <input 
                type="number"
                required
                className="w-full rounded-xl border-slate-200 shadow-sm px-4 py-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                value={binId}
                onChange={(e) => setBinId(e.target.value ? Number(e.target.value) : '')}
                placeholder="e.g. 12"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
              <textarea 
                required
                className="w-full rounded-xl border-slate-200 shadow-sm px-4 py-3 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                rows={4}
                value={complaintDesc}
                onChange={(e) => setComplaintDesc(e.target.value)}
                placeholder="Describe the issue..."
              />
            </div>

            <button type="submit" className="w-full bg-blue-600 text-white font-semibold py-3 px-4 rounded-xl hover:bg-blue-700 transition-colors shadow-md shadow-blue-200 active:scale-[0.98]">
              Submit Report
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
