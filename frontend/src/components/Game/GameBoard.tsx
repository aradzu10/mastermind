import { useState, useEffect, useRef } from "react";
import { useGameStore } from "../../store/gameStore";
import GuessInput from "./GuessInput";
import GuessHistory from "./GuessHistory";
import { UserBadge } from "../Auth/UserBadge";
import { GameModeSelector } from "./GameModeSelector";
import type { GameMode } from "../../types/game";

export default function GameBoard() {
  const { game, loading, error, createGame, resetGame, opponentGuess, opponentThinking } =
    useGameStore();
  const [showModeSelector, setShowModeSelector] = useState(!game);
  const previousOpponentGuessCountRef = useRef(0);

  const handleStartGame = async (mode: GameMode, playerSecret?: string) => {
    await createGame(mode, playerSecret, mode === "ai" ? "easy" : undefined);
    setShowModeSelector(false);
  };

  const handleNewGame = () => {
    resetGame();
    setShowModeSelector(true);
  };

  useEffect(() => {
    if (!game || game.game_mode === "single" || game.winner_id !== null) {
      return;
    }

    if (opponentThinking) {
      opponentGuess();

      const pollInterval = setInterval(() => {
        opponentGuess();
      }, 10000);

      return () => clearInterval(pollInterval);
    }
  }, [opponentThinking]);

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

  const isPvPMode = game?.game_mode !== "single";
  const opponentEmoji = game?.game_mode === "ai" ? "🤖" : "";
  const playerWon = game?.winner_id === game?.self_id;
  const opponentWon = game?.winner_id === game?.opponent_id;
  const gameOver = game?.winner_id !== null;

  if (!game) {
    return null;
  }

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
                <h1 className="text-3xl font-bold">
                  {isPvPMode
                    ? `You ⚔️ ${game?.opponent_name} ${opponentEmoji}`
                    : "🎯 Single Player"}
                </h1>
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
          {gameOver && (
            <div
              className={`p-4 ${playerWon ? "bg-green-100 border-green-300" : opponentWon ? "bg-red-100 border-red-300" : "bg-blue-100 border-blue-300"} border-b-2`}
            >
              <div
                className={`font-semibold text-lg ${playerWon ? "text-green-800" : opponentWon ? "text-red-800" : "text-blue-800"}`}
              >
                {playerWon &&
                  !opponentWon &&
                  `🎉 You won in ${game.self_guesses.length} attempts!`}
                {opponentWon &&
                  !playerWon &&
                  `😔 Opponent won! It guessed your code in ${game.opponent_guesses?.length || 0} attempts.`}
                {playerWon &&
                  opponentWon &&
                  `🤝 It's a tie! You both guessed the codes!`}
              </div>
              {game.self_secret && (
                <p className="text-sm text-gray-700 mt-2">
                  Your secret was:{" "}
                  <span className="font-mono font-bold text-lg">
                    {game.self_secret}
                  </span>
                </p>
              )}
            </div>
          )}

          <div className="p-8">
            {isPvPMode ? (
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
                      Attempts:{" "}
                      <span className="font-bold text-indigo-900">
                        {game.self_guesses.length}
                      </span>
                    </div>
                    {gameOver && playerWon && (
                      <div className="mt-2 text-green-600 font-semibold">
                        ✓ You cracked it!
                      </div>
                    )}
                  </div>

                  <GuessInput disabled={gameOver} />
                  <GuessHistory
                    guesses={game.self_guesses}
                    title="Your Guesses"
                  />
                </div>

                {/* Opponent Side */}
                <div className="space-y-4">
                  <div className="bg-purple-50 rounded-lg p-4 border-2 border-purple-200">
                    <h2 className="text-xl font-bold text-purple-900 mb-2">
                      {opponentEmoji} {game?.opponent_name}
                    </h2>
                    <p className="text-sm text-purple-700 mb-2">
                      Opponent is guessing your secret code
                    </p>
                    <div className="text-purple-600">
                      Attempts:{" "}
                      <span className="font-bold text-purple-900">
                        {game.opponent_guesses?.length || 0}
                      </span>
                    </div>
                    {gameOver && opponentWon && (
                      <div className="mt-2 text-red-600 font-semibold">
                        ✓ Opponent cracked it!
                      </div>
                    )}
                  </div>

                  <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                    <div className="flex items-baseline gap-3">
                      <p className="text-sm text-purple-700 mb-1 font-semibold">
                        Your Secret Code:
                      </p>
                      <p className="text-xl font-mono font-bold text-purple-900 tracking-wider">
                        {game.opponent_secret}
                      </p>
                    </div>
                  </div>

                  <GuessHistory
                    guesses={game.opponent_guesses || []}
                    title="Opponent's Guesses"
                    isOpponent={true}
                  />
                </div>
              </div>
            ) : (
              // Single View for Single Player Mode
              <div className="max-w-2xl mx-auto">
                <div className="mb-8">
                  <div className="text-gray-600 mb-4">
                    Attempts:{" "}
                    <span className="font-bold text-gray-800">
                      {game.self_guesses.length}
                    </span>
                  </div>
                  <GuessInput disabled={gameOver} />
                </div>

                <GuessHistory guesses={game.self_guesses} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
