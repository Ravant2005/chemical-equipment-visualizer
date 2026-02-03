import axios from 'axios';

// API URL configuration
// For development: defaults to http://localhost:8000/api
// For production: set VITE_API_URL environment variable
const getApiBaseUrl = () => {
  // Check for environment variable
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) {
    // Remove trailing slash if present
    return envUrl.replace(/\/$/, '');
  }
  // Default to localhost for development
  return 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

console.log(`API Base URL: ${API_BASE_URL}`); // Debug log

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
    config.headers.Authorization = `Token ${token}`;
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
    api.post('/auth/register/', { username, email, password }),
  
  login: (username, password) =>
    api.post('/auth/login/', { username, password }),
  
  logout: () =>
    api.post('/auth/logout/'),
  
  getCurrentUser: () =>
    api.get('/auth/user/'),
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