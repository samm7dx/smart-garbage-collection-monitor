import axios from 'axios';

const configuredBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api';
const API_URL = configuredBaseUrl.replace(/\/+$/, '');

export const api = axios.create({
  baseURL: API_URL,
});

export interface Bin {
  id: number;
  name: string;
  area: string;
  latitude: number;
  longitude: number;
  capacity: number;
  current_fill_percentage: number;
  collection_frequency_days: number;
  scheduled_collection_time: string;
  status: 'NORMAL' | 'DELAYED' | 'MISSED' | 'OVERFLOW_RISK';
  created_at: string;
}

export interface Complaint {
  id: number;
  bin_id: number;
  area: string;
  description: string;
  reported_at: string;
  status: 'OPEN' | 'RESOLVED';
}

export interface AnalyticsSummary {
  total_bins: number;
  on_time_collections: number;
  delayed_collections: number;
  missed_collections: number;
  high_risk_bins: number;
  open_complaints: number;
}

export interface PredictionResponse {
  bin_id: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_probability: number;
}

export const getBins = () => api.get<Bin[]>('/bins').then((res) => res.data);
export const getBin = (id: number) => api.get<Bin>(`/bins/${id}`).then((res) => res.data);
export const getCollections = () => api.get('/collections').then((res) => res.data);
export const getComplaints = () => api.get<Complaint[]>('/complaints').then((res) => res.data);
export const getAnalytics = () => api.get<AnalyticsSummary>('/analytics/summary').then((res) => res.data);
export const submitComplaint = (data: {bin_id: number, area: string, description: string}) => api.post<Complaint>('/complaints', data).then(res => res.data);
export const updateComplaintStatus = (id: number, status: string) => api.put<Complaint>(`/complaints/${id}`, {status}).then(res => res.data);
export const recordCollection = (binId: number) => api.post(`/collections/record/${binId}`).then(res => res.data);
export const updateCollection = (id: number, data: { actual_collection_date?: string; actual_collection_time?: string }) => api.put(`/collections/${id}`, data).then(res => res.data);
export const predictRisk = (id: number) => api.post<PredictionResponse>(`/predictions/bin/${id}`).then((res) => res.data);
