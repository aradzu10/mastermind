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
}

export interface GameGuessResponse {
  game_id: number;
  guess: string;
  exact: number;
  wrong_pos: number;
  is_winner: boolean;
  attempts: number;
  game_over: boolean;
}
