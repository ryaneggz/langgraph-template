import axios, { AxiosResponse } from 'axios';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your API base URL
  timeout: 10000, // Set request timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
apiClient.interceptors.request.use(
  (config: any) => {
    const token = localStorage.getItem('token'); // Replace with your token logic
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: any) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access, e.g., logout user
      console.error('Unauthorized! Redirecting to login...');
      localStorage.removeItem('token'); // Clear token
      window.location.href = '/login'; // Redirect to login page
    }
    return Promise.reject(error);
  }
);

export default apiClient;
