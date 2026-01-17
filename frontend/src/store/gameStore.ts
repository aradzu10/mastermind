import { create } from 'zustand';
import type { Game, GuessRecord, GameMode } from '../types/game';
import { gameApi } from '../services/api';

interface GameState {
  game: Game | null;
  loading: boolean;
  error: string | null;
  currentGuess: string;

  setCurrentGuess: (guess: string) => void;
  createGame: (mode?: GameMode, playerSecret?: string) => Promise<void>;
  makeGuess: (guess: string) => Promise<void>;
  resetGame: () => void;
}

export const useGameStore = create<GameState>((set, get) => ({
  game: null,
  loading: false,
  error: null,
  currentGuess: '',

  setCurrentGuess: (guess: string) => {
    if (guess.length <= 4 && /^\d*$/.test(guess)) {
      set({ currentGuess: guess });
    }
  },

  createGame: async (mode: GameMode = 'single', playerSecret?: string) => {
    set({ loading: true, error: null });
    try {
      const game = await gameApi.createGame(mode, playerSecret);
      set({ game, loading: false, currentGuess: '' });
    } catch (error) {
      set({ error: 'Failed to create game', loading: false });
    }
  },

  makeGuess: async (guess: string) => {
    const { game } = get();
    if (!game || game.won || guess.length !== 4) return;

    set({ loading: true, error: null });
    try {
      const result = await gameApi.makeGuess(game.id, guess);

      const newGuess: GuessRecord = {
        guess: result.guess,
        exact: result.exact,
        wrong_pos: result.wrong_pos,
      };

      // Handle AI move if present
      const aiGuesses = game.ai_guesses || [];
      if (result.ai_move) {
        aiGuesses.push({
          guess: result.ai_move.ai_guess,
          exact: result.ai_move.exact,
          wrong_pos: result.ai_move.wrong_pos,
        });
      }

      set({
        game: {
          ...game,
          guesses: [...game.guesses, newGuess],
          ai_guesses: aiGuesses,
          attempts: result.attempts,
          won: result.is_winner,
          ai_won: result.ai_move?.ai_won,
        },
        currentGuess: '',
        loading: false,
      });
    } catch (error) {
      set({ error: 'Failed to make guess', loading: false });
    }
  },

  resetGame: () => {
    set({ game: null, currentGuess: '', error: null });
  },
}));
