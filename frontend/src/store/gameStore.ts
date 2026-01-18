import { create } from "zustand";
import type { Game, GameMode } from "../types/game";
import { gameApi } from "../services/api";

// Helper function to calculate if opponent is thinking
const calculateOpponentThinking = (game: Game): boolean => {
  if (game.game_mode === "single" || game.winner_id !== null) {
    return false;
  }
  return (
    game.opponent_id !== undefined && game.current_turn === game.opponent_id
  );
};

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
  abandonGame: () => Promise<void>;
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
      const gameWithElo = {
        ...game,
        old_self_elo: game.self_elo,
      };
      set({
        game: gameWithElo,
        loading: false,
        currentGuess: "",
        opponentThinking: calculateOpponentThinking(gameWithElo),
      });
    } catch (error) {
      set({ error: "Failed to create game", loading: false });
    }
  },

  getGame: async (gameId: number) => {
    const { game } = get();
    try {
      const result = await gameApi.getGame(gameId);
      const gameWithElo = {
        ...result,
        old_self_elo: game?.old_self_elo || result.self_elo,
      };
      set({
        game: gameWithElo,
        opponentThinking: calculateOpponentThinking(result),
      });
      return result;
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
      const gameWithElo = {
        ...result,
        old_self_elo: game?.old_self_elo || result.self_elo,
      };
      set({
        game: gameWithElo,
        currentGuess: "",
        loading: false,
        opponentThinking: calculateOpponentThinking(gameWithElo),
      });
    } catch (error) {
      set({ error: "Failed to make guess", loading: false });
    }
  },

  opponentGuess: async () => {
    const { game } = get();
    if (!game || game.winner_id || game.game_mode === "single") return;

    try {
      const result = await gameApi.opponentGuess(game.id);

      const oppGuesses =
        (result.opponent_guesses?.length || 0) >
        (game.opponent_guesses?.length || 0)
          ? result.opponent_guesses
          : game.opponent_guesses;

      const gameWithElo = {
        ...result,
        opponent_guesses: oppGuesses,
        old_self_elo: game?.old_self_elo || result.self_elo,
      };
      set({
        game: gameWithElo,
        loading: false,
        opponentThinking: calculateOpponentThinking(gameWithElo),
      });
    } catch (error) {
      set({ error: "Failed to get opponent's guess", loading: false });
    }
  },

  abandonGame: async () => {
    const { game } = get();
    if (!game) return;

    if (game.status !== "in_progress" || game.game_mode === "single") {
      return;
    }

    try {
      await gameApi.abandonGame(game.id);
    } catch (error) {
      console.error("Failed to abandon game:", error);
    }
  },

  resetGame: () => {
    set({ game: null, currentGuess: "", error: null });
  },
}));
