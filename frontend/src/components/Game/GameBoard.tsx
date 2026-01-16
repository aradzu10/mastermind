import { useEffect } from 'react';
import { useGameStore } from '../../store/gameStore';
import GuessInput from './GuessInput';
import GuessHistory from './GuessHistory';

export default function GameBoard() {
  const { game, loading, error, createGame, resetGame } = useGameStore();

  useEffect(() => {
    if (!game && !loading) {
      createGame();
    }
  }, []);

  const handleNewGame = () => {
    resetGame();
    createGame();
  };

  if (loading && !game) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading game...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-xl text-red-600 mb-4">{error}</div>
          <button
            onClick={handleNewGame}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Mastermind</h1>
            <button
              onClick={handleNewGame}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold
                         hover:bg-gray-300 transition-colors"
            >
              New Game
            </button>
          </div>

          {game?.won && (
            <div className="mb-6 p-4 bg-green-100 border border-green-300 rounded-lg">
              <div className="text-green-800 font-semibold text-lg">
                🎉 Congratulations! You won in {game.attempts} attempts!
              </div>
            </div>
          )}

          <div className="mb-8">
            <div className="text-gray-600 mb-4">
              Attempts: <span className="font-bold text-gray-800">{game?.attempts || 0}</span>
            </div>
            <GuessInput />
          </div>

          <GuessHistory guesses={game?.guesses || []} />
        </div>
      </div>
    </div>
  );
}
