import axios from 'axios';

// API URL configuration
// Supports both local development and production deployment
const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Only log in development to avoid exposing production URLs in console
if (import.meta.env.DEV) {
  console.log(`API Base URL: ${API_BASE_URL}`);
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, logout user
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (username, email, password) =>
    api.post('/accounts/auth/register/', { username, email, password }),
  
  login: (username, password) =>
    api.post('/accounts/auth/login/', { username, password }),
  
  logout: () =>
    api.post('/accounts/auth/logout/'),
  
  getCurrentUser: () =>
    api.get('/accounts/auth/user/'),
};

// Dataset API
export const datasetAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/datasets/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getAll: () =>
    api.get('/datasets/'),
  
  getById: (id) =>
    api.get(`/datasets/${id}/`),
  
  getSummary: (id) =>
    api.get(`/datasets/${id}/summary/`),
  
  getHistory: () =>
    api.get('/datasets/history/'),
  
  delete: (id) =>
    api.delete(`/datasets/${id}/`),
  
  generateReport: (id) =>
    api.get(`/datasets/${id}/generate_report/`, {
      responseType: 'blob',
      headers: {
        'Accept': 'application/pdf'
      }
    }),
};

export default api;
