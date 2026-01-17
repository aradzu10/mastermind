import { useState } from 'react';
import { useGameStore } from '../../store/gameStore';
import GuessInput from './GuessInput';
import GuessHistory from './GuessHistory';
import { UserBadge } from '../Auth/UserBadge';
import { GameModeSelector } from './GameModeSelector';
import type { GameMode } from '../../types/game';

export default function GameBoard() {
  const { game, loading, error, createGame, resetGame } = useGameStore();
  const [showModeSelector, setShowModeSelector] = useState(!game);

  const handleStartGame = async (mode: GameMode, playerSecret?: string) => {
    await createGame(mode, playerSecret);
    setShowModeSelector(false);
  };

  const handleNewGame = () => {
    resetGame();
    setShowModeSelector(true);
  };

  // Show mode selector if no game
  if (showModeSelector || (!game && !loading)) {
    return <GameModeSelector onStartGame={handleStartGame} />;
  }

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

  const isAIMode = game?.game_mode === 'ai';
  const playerWon = game?.won || false;
  const aiWon = game?.ai_won || false;
  const gameOver = playerWon || aiWon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header with user badge */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-4">
          <UserBadge />
        </div>

        <div className="bg-white rounded-lg shadow-2xl overflow-hidden">
          {/* Title Bar */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold">Mastermind</h1>
                <p className="text-indigo-100 mt-1">
                  {isAIMode ? '🤖 AI Opponent Mode' : '🎯 Single Player'}
                </p>
              </div>
              <button
                onClick={handleNewGame}
                className="px-6 py-3 bg-white text-indigo-600 rounded-lg font-semibold
                         hover:bg-indigo-50 transition-colors shadow-md"
              >
                New Game
              </button>
            </div>
          </div>

          {/* Game Over Message */}
          {gameOver && game && (
            <div className={`p-4 ${playerWon ? 'bg-green-100 border-green-300' : aiWon ? 'bg-red-100 border-red-300' : 'bg-blue-100 border-blue-300'} border-b-2`}>
              <div className={`font-semibold text-lg ${playerWon ? 'text-green-800' : aiWon ? 'text-red-800' : 'text-blue-800'}`}>
                {playerWon && !aiWon && `🎉 You won in ${game.attempts} attempts!`}
                {aiWon && !playerWon && `😔 AI won! It guessed your code in ${game.ai_guesses?.length || 0} attempts.`}
                {playerWon && aiWon && `🤝 It's a tie! You both guessed the codes!`}
              </div>
              {game.player_secret && (
                <p className="text-sm text-gray-700 mt-2">
                  Your secret was: <span className="font-mono font-bold text-lg">{game.player_secret}</span>
                </p>
              )}
            </div>
          )}

          <div className="p-8">
            {isAIMode ? (
              // Dual View for AI Mode
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Player Side */}
                <div className="space-y-4">
                  <div className="bg-indigo-50 rounded-lg p-4 border-2 border-indigo-200">
                    <h2 className="text-xl font-bold text-indigo-900 mb-2">
                      👤 You
                    </h2>
                    <p className="text-sm text-indigo-700 mb-2">
                      Guess the computer's secret code
                    </p>
                    <div className="text-indigo-600">
                      Attempts: <span className="font-bold text-indigo-900">{game.attempts || 0}</span>
                    </div>
                    {playerWon && (
                      <div className="mt-2 text-green-600 font-semibold">✓ You cracked it!</div>
                    )}
                  </div>

                  <GuessInput disabled={gameOver} />
                  <GuessHistory guesses={game.guesses || []} title="Your Guesses" />
                </div>

                {/* AI Side */}
                <div className="space-y-4">
                  <div className="bg-purple-50 rounded-lg p-4 border-2 border-purple-200">
                    <h2 className="text-xl font-bold text-purple-900 mb-2">
                      🤖 AI Opponent
                    </h2>
                    <p className="text-sm text-purple-700 mb-2">
                      AI is guessing your secret code
                    </p>
                    <div className="text-purple-600">
                      Attempts: <span className="font-bold text-purple-900">{game.ai_guesses?.length || 0}</span>
                    </div>
                    {aiWon && (
                      <div className="mt-2 text-red-600 font-semibold">✓ AI cracked it!</div>
                    )}
                  </div>

                  <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                    <p className="text-sm text-purple-700">
                      {gameOver 
                        ? `Your secret: ${game.player_secret}`
                        : 'Your secret is hidden'}
                    </p>
                  </div>

                  <GuessHistory 
                    guesses={game.ai_guesses || []} 
                    title="AI's Guesses" 
                    isOpponent={true}
                  />
                </div>
              </div>
            ) : (
              // Single View for Single Player Mode
              <div className="max-w-2xl mx-auto">
                <div className="mb-8">
                  <div className="text-gray-600 mb-4">
                    Attempts: <span className="font-bold text-gray-800">{game?.attempts || 0}</span>
                  </div>
                  <GuessInput disabled={gameOver} />
                </div>

                <GuessHistory guesses={game?.guesses || []} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
