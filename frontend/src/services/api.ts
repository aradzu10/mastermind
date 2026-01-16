import axios from 'axios';
import type { Game, GameGuessResponse } from '../types/game';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const gameApi = {
  createGame: async (gameMode: string = 'single'): Promise<Game> => {
    const response = await api.post<Game>('/api/games/single', { game_mode: gameMode });
    return response.data;
  },

  getGame: async (gameId: number): Promise<Game> => {
    const response = await api.get<Game>(`/api/games/${gameId}`);
    return response.data;
  },

  makeGuess: async (gameId: number, guess: string): Promise<GameGuessResponse> => {
    const response = await api.post<GameGuessResponse>(`/api/games/${gameId}/guess`, { guess });
    return response.data;
  },
};
