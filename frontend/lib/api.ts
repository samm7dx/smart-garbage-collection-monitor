import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
});

export const getBins = () => api.get('/bins').then((res) => res.data);
export const getBin = (id: number) => api.get(`/bins/${id}`).then((res) => res.data);
export const getCollections = () => api.get('/collections').then((res) => res.data);
export const getComplaints = () => api.get('/complaints').then((res) => res.data);
export const getAnalytics = () => api.get('/analytics/summary').then((res) => res.data);
export const submitComplaint = (data: {bin_id: number, area: string, description: string}) => api.post('/complaints', data).then(res => res.data);
export const updateComplaintStatus = (id: number, status: string) => api.put(`/complaints/${id}`, {status}).then(res => res.data);
export const recordCollection = (data: any) => api.post('/collections', data).then(res => res.data);
export const updateCollection = (id: number, data: any) => api.put(`/collections/${id}`, data).then(res => res.data);
export const predictRisk = (id: number) => api.post(`/predictions/bin/${id}`).then((res) => res.data);
