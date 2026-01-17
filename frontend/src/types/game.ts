export interface GuessRecord {
  guess: string;
  exact: number;
  wrong_pos: number;
}

export interface Game {
  id: number;
  attempts: number;
  won: boolean;
  game_mode: string;
  guesses: GuessRecord[];
  completed_at: string | null;
  created_at: string;
  opponent_type: string;  // "none", "ai", "human"
  ai_guesses?: GuessRecord[];  // AI's guesses against player's secret
  player_secret?: string | null;  // Player's secret (for AI mode), hidden until game over
  ai_won?: boolean | null;  // Did the AI win?
}

export interface GameGuessResponse {
  game_id: number;
  guess: string;
  exact: number;
  wrong_pos: number;
  is_winner: boolean;
  attempts: number;
  game_over: boolean;
  ai_move?: {  // Present in AI mode
    ai_guess: string;
    exact: number;
    wrong_pos: number;
    ai_won: boolean;
  };
}

export type GameMode = 'single' | 'ai' | 'pvp';
