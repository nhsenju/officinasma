import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const callsApi = {
  getCalls: (params?: any) => api.get('/calls', { params }),
  getCall: (id: string) => api.get(`/calls/${id}`),
  updateCall: (id: string, data: any) => api.put(`/calls/${id}`, data),
  deleteCall: (id: string) => api.delete(`/calls/${id}`),
  getCallTranscript: (id: string) => api.get(`/calls/${id}/transcript`),
  addTagsToCall: (id: string, tags: string[]) => api.post(`/calls/${id}/tags`, tags),
};

export const transcriptsApi = {
  getTranscript: (id: string) => api.get(`/transcripts/${id}`),
  updateTranscript: (id: string, data: any) => api.put(`/transcripts/${id}`, data),
  deleteTranscript: (id: string) => api.delete(`/transcripts/${id}`),
  searchTranscripts: (params: any) => api.get('/transcripts/search', { params }),
};

export const authApi = {
  login: (credentials: { username: string; password: string }) => {
    // Create FormData for OAuth2 format
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  register: (userData: { username: string; email: string; password: string }) =>
    api.post('/auth/register', userData),
};

export const exportApi = {
  exportCalls: (format: string, filters?: any) =>
    api.post('/export/calls', { format, filters }),
  getExportStatus: (jobId: string) => api.get(`/export/${jobId}/status`),
  downloadExport: (jobId: string) => api.get(`/export/${jobId}/download`),
};

export const ingestApi = {
  ingestEmail: (data: FormData) => {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token non trovato. Effettua il login.');
    }
    
    // Per FormData, NON impostare Content-Type, lascia che il browser lo gestisca automaticamente
    return api.post('/ingest/email', data, {
      headers: {
        'Authorization': `Bearer ${token}`,
        // Rimuovi Content-Type per permettere al browser di impostare multipart/form-data
      },
      // Assicurati che axios non trasformi FormData in JSON
      transformRequest: [(data) => data], // Non trasformare FormData
    });
  },
  setupGmail: (credentials: { client_id: string; client_secret: string }) =>
    api.post('/ingest/gmail', credentials),
  setupOutlook: (credentials: { client_id: string; client_secret: string }) =>
    api.post('/ingest/outlook', credentials),
  getStatus: () => api.get('/ingest/status'),
};

// API per la gestione officina
export const appointmentsApi = {
  getAppointments: (params?: any) => api.get('/appointments', { params }),
  getAppointment: (id: number) => api.get(`/appointments/${id}`),
  createAppointment: (data: any) => api.post('/appointments', data),
  updateAppointment: (id: number, data: any) => api.put(`/appointments/${id}`, data),
  deleteAppointment: (id: number) => api.delete(`/appointments/${id}`),
};

export const customersApi = {
  getCustomers: (params?: any) => api.get('/customers', { params }),
  getCustomer: (id: number) => api.get(`/customers/${id}`),
  createCustomer: (data: any) => api.post('/customers', data),
  updateCustomer: (id: number, data: any) => api.put(`/customers/${id}`, data),
  deleteCustomer: (id: number) => api.delete(`/customers/${id}`),
  searchCustomers: (search: string) => api.get('/customers', { params: { search } }),
};

export const vehiclesApi = {
  getVehicles: (params?: any) => api.get('/vehicles', { params }),
  getVehicle: (id: number) => api.get(`/vehicles/${id}`),
  createVehicle: (data: any) => api.post('/vehicles', data),
  updateVehicle: (id: number, data: any) => api.put(`/vehicles/${id}`, data),
  deleteVehicle: (id: number) => api.delete(`/vehicles/${id}`),
  getVehiclesByCustomer: (customerId: number) => api.get('/vehicles', { params: { customer_id: customerId } }),
  searchVehicles: (search: string) => api.get('/vehicles', { params: { search } }),
};

export const servicesApi = {
  getServices: (params?: any) => api.get('/services', { params }),
  getService: (id: number) => api.get(`/services/${id}`),
  createService: (data: any) => api.post('/services', data),
  updateService: (id: number, data: any) => api.put(`/services/${id}`, data),
  deleteService: (id: number) => api.delete(`/services/${id}`),
  getServiceCategories: () => api.get('/services/categories'),
  getServicesByCategory: (category: string) => api.get('/services', { params: { category } }),
};

export const aiApi = {
  // Livestream monitoring
  startLivestream: (streamUrl: string, outputUrl?: string, options?: {
    enable_face_blur?: boolean;
    enable_plate_blur?: boolean;
    save_plate_images?: boolean;
  }) => api.post('/ai/livestream/start', { 
    stream_url: streamUrl, 
    output_url: outputUrl,
    ...options 
  }),
  stopLivestream: () => api.post('/ai/livestream/stop'),
  getLivestreamStatus: () => api.get('/ai/livestream/status'),
  
  // License plate detection
  detectPlate: (licensePlate: string) => api.post('/ai/plate/detect', { license_plate: licensePlate }),
  searchPlate: (licensePlate: string) => api.get(`/ai/plate/search/${licensePlate}`),
  
  // Detections and stats
  getRecentDetections: (limit?: number) => api.get('/ai/detections/recent', { params: { limit } }),
  getAiStats: () => api.get('/ai/stats'),
  
  // Plate images
  getPlateImages: () => api.get('/ai/plates/images'),
  getPlateImage: (filename: string) => api.get(`/ai/plates/images/${filename}`),
  deletePlateImage: (filename: string) => api.delete(`/ai/plates/images/${filename}`),
  
  // General AI endpoints
  getDetections: (params?: any) => api.get('/ai', { params }),
  getDetection: (id: number) => api.get(`/ai/${id}`),
  createDetection: (data: any) => api.post('/ai', data),
  updateDetection: (id: number, data: any) => api.put(`/ai/${id}`, data),
  deleteDetection: (id: number) => api.delete(`/ai/${id}`),
  getDetectionStats: (startDate?: string, endDate?: string) => 
    api.get('/ai/stats', { params: { start_date: startDate, end_date: endDate } }),
};
