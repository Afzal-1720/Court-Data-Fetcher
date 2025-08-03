import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Match your Flask server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const submitCase = (data) => api.post('/api/submit', data);
export const downloadPDF = (caseNumber) => api.get(`/api/download/${caseNumber}`, { responseType: 'blob' });

export default api;