import axios from 'axios';
import type { TokenResponse, GuestUserCreate, User } from '../types/auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const authAxios = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
authAxios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  createGuest: async (displayName: string): Promise<TokenResponse> => {
    const response = await authAxios.post<TokenResponse>("/api/auth/guest", {
      display_name: displayName,
    } as GuestUserCreate);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await authAxios.get<User>("/api/auth/me");
    return response.data;
  },

  logout: async (): Promise<void> => {
    await authAxios.post("/api/auth/logout");
  },
};
