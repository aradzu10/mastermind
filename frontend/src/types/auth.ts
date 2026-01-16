/**
 * Authentication type definitions
 */

export interface User {
  id: number;
  email: string | null;
  display_name: string;
  is_guest: boolean;
  elo_rating: number;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface GuestUserCreate {
  display_name: string;
}

export interface GoogleAuthRequest {
  google_id: string;
  email: string;
  display_name: string;
}
