import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getCurrentUser: () => api.get('/auth/me'),
};

// Listings API
export const listingsAPI = {
  getAll: (params) => api.get('/listings/', { params }),
  getOne: (id) => api.get(`/listings/${id}`),
  create: (data) => api.post('/listings/', data),
  update: (id, data) => api.put(`/listings/${id}`, data),
  delete: (id) => api.delete(`/listings/${id}`),
  getProvenance: (id) => api.get(`/listings/${id}/provenance`),
  getPriceRecommendation: (id) => api.get(`/listings/${id}/price-recommendation`),
};

// Matches API
export const matchesAPI = {
  findMatches: (preferences) => api.post('/matches/find', preferences),
  getMyMatches: () => api.get('/matches/'),
  getOne: (id) => api.get(`/matches/${id}`),
};

// Notifications API
export const notificationsAPI = {
  getAll: (params) => api.get('/notifications/', { params }),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
};

// Wallet API
export const walletAPI = {
  getBalance: () => api.get('/wallet/balance'),
  deposit: (data) => api.post('/wallet/deposit', data),
  withdraw: (data) => api.post('/wallet/withdraw', data),
  transfer: (recipientId, data) => api.post(`/wallet/transfer?recipient_id=${recipientId}`, data),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getUserStats: () => api.get('/analytics/users/stats'),
  getListingStats: () => api.get('/analytics/listings/stats'),
  getMarketTrends: () => api.get('/analytics/market/trends'),
};

// Logistics API
export const logisticsAPI = {
  create: (data) => api.post('/logistics/', data),
  getAll: () => api.get('/logistics/'),
  getOne: (id) => api.get(`/logistics/${id}`),
  updateStatus: (id, status, trackingNumber) => 
    api.put(`/logistics/${id}/status?status=${status}${trackingNumber ? `&tracking_number=${trackingNumber}` : ''}`),
};

export default api;
