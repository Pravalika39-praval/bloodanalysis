import { API_BASE_URL, API_ENDPOINTS } from '@/config/api';

// Helper to get auth token
const getAuthToken = () => {
  return localStorage.getItem('auth_token');
};

// Helper to make API requests
const apiRequest = async (endpoint, options = {}) => {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token && !options.skipAuth) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(error.message || `HTTP ${response.status}`);
  }

  return response.json();
};

// Auth API
export const authAPI = {
  signup: async (email, password, fullName) => {
    const data = await apiRequest(API_ENDPOINTS.SIGNUP, {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({ email, password, full_name: fullName }),
    });
    
    // Store token
    if (data.token) {
      localStorage.setItem('auth_token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    
    return data;
  },

  login: async (email, password) => {
    const data = await apiRequest(API_ENDPOINTS.LOGIN, {
      method: 'POST',
      skipAuth: true,
      body: JSON.stringify({ email, password }),
    });
    
    // Store token
    if (data.token) {
      localStorage.setItem('auth_token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    
    return data;
  },

  logout: async () => {
    try {
      await apiRequest(API_ENDPOINTS.LOGOUT, {
        method: 'POST',
      });
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser: async () => {
    // Try to get from localStorage first
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      return JSON.parse(storedUser);
    }
    
    // Fetch from API
    const user = await apiRequest(API_ENDPOINTS.GET_USER);
    localStorage.setItem('user', JSON.stringify(user));
    return user;
  },

  isAuthenticated: () => {
    return !!getAuthToken();
  },
};

// Reports API
export const reportsAPI = {
  uploadReport: async (file) => {
    const token = getAuthToken();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.UPLOAD_REPORT}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Upload failed' }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  },

  analyzeReport: async (parameters) => {
    return apiRequest(API_ENDPOINTS.ANALYZE_REPORT, {
      method: 'POST',
      body: JSON.stringify({ parameters }),
    });
  },

  getHistory: async () => {
    const data = await apiRequest(API_ENDPOINTS.GET_HISTORY);
    return data.reports || [];
  },

  getReport: async (reportId) => {
    return apiRequest(`${API_ENDPOINTS.GET_REPORT}/${reportId}`);
  },
};

// Parameters API
export const parametersAPI = {
  getParameters: async () => {
    const data = await apiRequest(API_ENDPOINTS.GET_PARAMETERS);
    return data.parameters || [];
  },
};
