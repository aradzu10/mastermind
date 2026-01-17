import axios from 'axios';
import type { Game } from "../types/game";

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear auth and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const gameApi = {
  createGame: async (
    gameMode: string,
    playerSecret?: string,
    aiDifficulty?: string
  ): Promise<Game> => {
    const response = await api.post<Game>("/api/games/new", {
      game_mode: gameMode,
      player_secret: playerSecret,
      ai_difficulty: aiDifficulty,
    });
    return response.data;
  },

  getGame: async (gameId: number): Promise<Game> => {
    const response = await api.get<Game>(`/api/games/${gameId}`);
    return response.data;
  },

  makeGuess: async (gameId: number, guess: string): Promise<Game> => {
    const response = await api.post<Game>(`/api/games/${gameId}/guess`, {
      guess,
    });
    return response.data;
  },

  opponentGuess: async (gameId: number): Promise<Game> => {
    const response = await api.post<Game>(
      `/api/games/${gameId}/opponent_guess`
    );
    return response.data;
  },
};
