export interface GuessRecord {
  guess: string;
  exact: number;
  wrong_pos: number;
}

export interface Game {
  id: number;
  game_mode: string;

  self_id: number;
  self_name: string;
  self_secret: string | null; // Hidden until game over
  self_guesses: GuessRecord[];
  self_elo?: number;
  old_self_elo?: number; // ELO before game completion

  winner_id: number | null;
  created_at: string;
  completed_at: string | null;

  // PvP specific fields
  opponent_id?: number | null;
  opponent_name?: string | null;
  opponent_secret?: string | null;
  opponent_guesses?: GuessRecord[];
  opponent_elo?: number;
  old_opponent_elo?: number; // ELO before game completion
  current_turn?: number;
  status?: "waiting" | "in_progress" | "completed" | "abandoned";
  started_at?: string;

  // AI specific fields
  ai_difficulty?: string | null;
}

export type GameMode = 'single' | 'ai' | 'pvp';
