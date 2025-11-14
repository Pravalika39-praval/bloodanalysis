// Flask API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  SIGNUP: '/auth/signup',
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
  GET_USER: '/auth/user',
  
  // Reports
  UPLOAD_REPORT: '/reports/upload',
  ANALYZE_REPORT: '/reports/analyze',
  GET_HISTORY: '/reports/history',
  GET_REPORT: '/reports',
  
  // Parameters
  GET_PARAMETERS: '/parameters',
};
