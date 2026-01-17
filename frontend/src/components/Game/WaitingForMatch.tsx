import { useEffect } from 'react';
import { useGameStore } from '../../store/gameStore';

interface WaitingForMatchProps {
  gameId: number;
  playerSecret: string;
  onCancel: () => void;
}

export function WaitingForMatch({ gameId, playerSecret, onCancel }: WaitingForMatchProps) {
  const { getGame, game } = useGameStore();

  useEffect(() => {
    const pollInterval = setInterval(async () => {
      await getGame(gameId);

      // Check if opponent joined (polling will stop when GameBoard renders instead)
      if (game?.status === 'in_progress' && game?.opponent_id) {
        clearInterval(pollInterval);
      }
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(pollInterval);
  }, [gameId, getGame, game?.status, game?.opponent_id]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center">
        <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Multiplayer Match
        </h1>

        {/* Animated Sword */}
        <div className="text-8xl mb-6 animate-pulse">⚔️</div>

        <p className="text-xl text-gray-700 mb-4 font-semibold">
          Waiting for opponent...
        </p>

        <div className="bg-purple-50 rounded-lg p-4 mb-6 border-2 border-purple-200">
          <p className="text-sm text-purple-700 mb-2">Your Secret Code:</p>
          <p className="text-3xl font-mono font-bold text-purple-900 tracking-wider">
            {playerSecret}
          </p>
          <p className="text-xs text-purple-600 mt-2">
            Your opponent will try to guess this code
          </p>
        </div>

        {/* ELO display */}
        {game?.self_elo && (
          <div className="text-center mb-4">
            <p className="text-sm text-gray-600">
              Your ELO: <span className="font-bold text-gray-800">{game.self_elo}</span>
            </p>
          </div>
        )}

        <div className="flex items-center justify-center space-x-2 mb-6">
          <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-3 h-3 bg-pink-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>

        <button
          onClick={onCancel}
          className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
