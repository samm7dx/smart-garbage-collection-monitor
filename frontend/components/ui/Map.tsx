'use client';

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { useEffect, useState } from 'react';

const defaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const redIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const orangeIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

interface Bin {
  id: number;
  name: string;
  area: string;
  latitude: number;
  longitude: number;
  status: string;
  current_fill_percentage: number;
}

export default function Map({ bins, onPredict }: { bins: Bin[], onPredict?: (id: number) => void }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div className="h-full bg-slate-100 rounded-xl animate-pulse"></div>;

  return (
    <MapContainer center={[12.9716, 77.5946]} zoom={12} className="h-full w-full rounded-xl z-0">
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      {bins.map((bin) => {
        let icon = defaultIcon;
        if (bin.status === 'OVERFLOW_RISK' || bin.status === 'MISSED') icon = redIcon;
        else if (bin.status === 'DELAYED') icon = orangeIcon;

        return (
          <Marker key={bin.id} position={[bin.latitude, bin.longitude]} icon={icon}>
            <Popup>
              <div className="p-1 min-w-[180px]">
                <h3 className="font-bold text-base mb-1">{bin.name} (ID: {bin.id})</h3>
                <p className="text-sm text-slate-600 mb-2">{bin.area}</p>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium">Fill Level:</span>
                  <span className={`text-sm font-bold ${bin.current_fill_percentage > 80 ? 'text-red-600' : 'text-green-600'}`}>
                    {bin.current_fill_percentage.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium">Status:</span>
                  <span className="text-xs px-2 py-0.5 bg-slate-100 rounded-md font-medium">
                    {bin.status}
                  </span>
                </div>
                {onPredict && (
                  <button 
                    onClick={() => onPredict(bin.id)}
                    className="w-full bg-blue-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                  >
                    Predict Risk
                  </button>
                )}
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
