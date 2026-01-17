import { create } from 'zustand';
import type { Game, GameMode } from '../types/game';
import { gameApi } from '../services/api';

interface GameState {
  game: Game | null;
  loading: boolean;
  error: string | null;
  currentGuess: string;
  opponentThinking: boolean;

  setCurrentGuess: (guess: string) => void;
  createGame: (
    mode: GameMode,
    playerSecret?: string,
    aiDifficulty?: string
  ) => Promise<void>;
  getGame: (gameId: number) => Promise<Game>;
  makeGuess: (guess: string) => Promise<void>;
  opponentGuess: () => Promise<void>;
  resetGame: () => void;
}

export const useGameStore = create<GameState>((set, get) => ({
  game: null,
  loading: false,
  error: null,
  currentGuess: "",
  opponentThinking: false,

  setCurrentGuess: (guess: string) => {
    if (guess.length <= 4 && /^\d*$/.test(guess)) {
      set({ currentGuess: guess });
    }
  },

  createGame: async (
    mode: GameMode,
    playerSecret?: string,
    aiDifficulty?: string
  ) => {
    set({ loading: true, error: null });
    try {
      const game = await gameApi.createGame(mode, playerSecret, aiDifficulty);
      set({
        game: {
          ...game,
          old_self_elo: game.self_elo,
          old_opponent_elo: game.opponent_elo,
        },
        loading: false,
        currentGuess: "",
        opponentThinking:
          game.opponent_id === undefined
            ? false
            : game.current_turn === game.opponent_id,
      });
    } catch (error) {
      set({ error: "Failed to create game", loading: false });
    }
  },

  getGame: async (gameId: number) => {
    try {
      const game = await gameApi.getGame(gameId);
      set({ game });
      return game;
    } catch (error) {
      set({ error: "Failed to get game" });
      throw error;
    }
  },

  makeGuess: async (guess: string) => {
    const { game } = get();
    if (!game || game.winner_id || guess.length !== 4) return;

    set({ loading: true, error: null });
    try {
      const result = await gameApi.makeGuess(game.id, guess);

      set({
        game: {
          ...game,
          self_guesses: [...result.self_guesses],
          self_elo: result.self_elo,
          self_secret: result.self_secret,
          opponent_elo: result.opponent_elo,
          old_self_elo: game.old_self_elo ?? game.self_elo,
          old_opponent_elo: game.old_opponent_elo ?? game.opponent_elo,
          winner_id: result.winner_id,
          completed_at: result.completed_at,
          current_turn: result.current_turn,
        },
        currentGuess: "",
        loading: false,
        opponentThinking:
          game.game_mode !== "single" && result.winner_id === null,
      });
    } catch (error) {
      set({ error: "Failed to make guess", loading: false });
    }
  },

  opponentGuess: async () => {
    const { game } = get();
    if (!game || game.winner_id || game.game_mode === "single") return;

    // set({ loading: true, error: null });
    try {
      const result = await gameApi.opponentGuess(game.id);

      if (
        (result.opponent_guesses?.length || 0) >
          (game.opponent_guesses?.length || 0) ||
        result.winner_id !== null
      ) {
        console.log(result);
        console.log(game);
        set({
          game: {
            ...game,
            opponent_guesses: [...(result.opponent_guesses || [])],
            self_elo: result.self_elo,
            self_secret: result.self_secret,
            opponent_elo: result.opponent_elo,
            old_self_elo: game.old_self_elo ?? game.self_elo,
            old_opponent_elo: game.old_opponent_elo ?? game.opponent_elo,
            winner_id: result.winner_id,
            completed_at: result.completed_at,
            current_turn: result.current_turn,
          },
          loading: false,
          opponentThinking: false,
        });
      } else {
        // set({
        //   loading: false,
        // });
      }
    } catch (error) {
      set({ error: "Failed to get opponent's guess", loading: false });
    }
  },

  resetGame: () => {
    set({ game: null, currentGuess: "", error: null });
  },
}));
