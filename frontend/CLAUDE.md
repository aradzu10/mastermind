# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Frontend Architecture

React + TypeScript + Vite + Tailwind CSS application using Zustand for state management.

```
React Components (components/)
  ↓
Zustand Store (store/) - Global state management
  ↓
API Service (services/) - Axios HTTP client
  ↓
Backend API
```

## Commands

```bash
# From frontend directory
npm install              # Install dependencies
npm run dev              # Start dev server (http://localhost:5173)
npm run build            # Production build
npm run lint             # Run ESLint
npm run preview          # Preview production build
```

## Directory Structure

- `src/components/Game/` - Game UI components
  - `GameBoard.tsx` - Main game container, orchestrates game flow
  - `GuessInput.tsx` - 4-digit input with validation
  - `GuessHistory.tsx` - Display past guesses with feedback badges
- `src/store/` - Zustand state management
  - `gameStore.ts` - Global game state and actions
- `src/services/` - API integration
  - `api.ts` - Axios client for backend communication
- `src/types/` - TypeScript type definitions
  - `game.ts` - Game, GuessRecord, GameGuessResponse interfaces
- `App.tsx` - Root component

## State Management (Zustand)

Centralized state in `src/store/gameStore.ts`:

```typescript
interface GameState {
  game: Game | null;           // Current game data
  loading: boolean;            // API request status
  error: string | null;        // Error messages
  currentGuess: string;        // Input field value

  setCurrentGuess: (guess: string) => void;
  createGame: () => Promise<void>;
  makeGuess: (guess: string) => Promise<void>;
  resetGame: () => void;
}
```

### Usage in Components

```typescript
import { useGameStore } from '../../store/gameStore';

function MyComponent() {
  const { game, loading, createGame } = useGameStore();
  // Component logic
}
```

## API Integration

All backend requests go through `src/services/api.ts`:

```typescript
gameApi.createGame()                    // POST /api/games/single
gameApi.getGame(gameId)                 // GET /api/games/{id}
gameApi.makeGuess(gameId, guess)        // POST /api/games/{id}/guess
```

### API Proxy
Vite proxies `/api/*` requests to `http://localhost:8000` (configured in `vite.config.ts`). This avoids CORS issues during development.

## Component Architecture

### GameBoard.tsx
Main container component:
- Auto-creates game on mount
- Displays win state banner
- Shows attempts counter
- Provides "New Game" button
- Handles loading and error states

### GuessInput.tsx
Controlled input component:
- Pattern validation (4 digits only)
- Disabled when loading or game won
- Submits on Enter key
- Integrates with Zustand store

### GuessHistory.tsx
Read-only display component:
- Maps over `game.guesses` array
- Green badges for exact matches
- Yellow badges for wrong position matches
- Numbered attempts

## TypeScript Types

### Game Interface
```typescript
interface Game {
  id: number;
  secret: string;
  attempts: number;
  won: boolean;
  game_mode: string;
  guesses: GuessRecord[];
  created_at: string;
}
```

### GuessRecord Interface
```typescript
interface GuessRecord {
  guess: string;      // "1234"
  exact: number;      // Correct digit, correct position
  wrong_pos: number;  // Correct digit, wrong position
}
```

## Styling with Tailwind CSS

All styling uses Tailwind utility classes:
- Responsive design: `md:`, `lg:` prefixes
- Layout: Flexbox and Grid utilities
- Colors: `bg-blue-600`, `text-gray-800`
- Spacing: `p-4`, `mb-8`, `gap-2`
- Hover states: `hover:bg-blue-700`

### Configuration
- `tailwind.config.js` - Tailwind settings
- `postcss.config.js` - PostCSS plugins (Tailwind + Autoprefixer)
- `src/index.css` - Tailwind directives (@tailwind base/components/utilities)

## Development Workflow

1. Start backend: `docker-compose up -d postgres && uvicorn backend.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:5173`
4. Vite hot-reloads on file changes
5. Check console for errors, use React DevTools for debugging

## Adding New Features

### New API Endpoint
1. Add method to `src/services/api.ts`
2. Update TypeScript types in `src/types/`
3. Add Zustand store actions in `src/store/gameStore.ts`
4. Use in components

### New Component
1. Create in appropriate directory (e.g., `src/components/Game/`)
2. Import and use Zustand store hooks
3. Style with Tailwind classes
4. Export and import in parent component

### New State
1. Add to `GameState` interface in `src/store/gameStore.ts`
2. Initialize in store creation
3. Add setter actions as needed
4. Use via `useGameStore()` hook in components

## Environment Variables

Optional (set in `.env.local`):
- `VITE_API_URL` - Override backend URL (defaults to `http://localhost:8000`)

Vite exposes env vars prefixed with `VITE_` to the browser.

## Build Process

Development:
- Vite dev server with HMR
- TypeScript checking in editor
- ESLint for code quality

Production:
- `npm run build` → TypeScript compile + Vite bundle
- Output: `dist/` directory
- Static files ready for deployment (Nginx, Vercel, etc.)

## Important Notes

- All API responses are typed with TypeScript interfaces
- Zustand provides simpler state management than Redux/Context
- Vite is faster than Create React App (native ESM)
- Tailwind CSS v3 configured (not v4 - see PROGRESS.md)
- Components are functional with hooks (no class components)
- Use `useEffect` sparingly - Zustand handles most side effects
