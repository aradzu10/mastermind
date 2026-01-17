import { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";
import { useAuthStore } from "../../store/authStore";
import type { Game } from "../../types/game";

interface GameOverScreenProps {
  game: Game;
  onExit: () => void;
}

export function GameOverScreen({ game, onExit }: GameOverScreenProps) {
  const [animatingElo, setAnimatingElo] = useState(false);
  
  // Capture the initial ELO value once and keep it fixed
  const initialEloRef = useRef(game.self_elo);
  const oldElo = initialEloRef.current || -1;
  
  const [displayElo, setDisplayElo] = useState(oldElo);
  const [newElo, setNewElo] = useState(oldElo);
  const [eloChange, setEloChange] = useState(0);

  const playerWon = game.winner_id === game.self_id;
  const opponentWon = game.winner_id === game.opponent_id;
  const isTie = playerWon && opponentWon;

  const isPvPorAI = game.game_mode !== "single";

  useEffect(() => {
    if (game.self_elo !== oldElo) {
      const change = (game.self_elo || 0) - oldElo;
      setEloChange(change);
      setNewElo(game.self_elo || 0);
    }
  }, [game.self_elo, oldElo]);

  useEffect(() => {
    // Start ELO animation after a delay
    const startDelay = setTimeout(() => {
      setAnimatingElo(true);
    }, 1000);

    return () => clearTimeout(startDelay);
  }, []);

  // Animate ELO digit by digit
  useEffect(() => {
    if (!animatingElo || !isPvPorAI) return;

    const difference = newElo - oldElo;
    if (difference === 0) return;

    const duration = 1500; // Total animation time
    const steps = Math.abs(difference);
    const stepDuration = duration / steps;

    let currentStep = 0;
    const interval = setInterval(() => {
      currentStep++;
      const current = oldElo + Math.floor((difference * currentStep) / steps);
      setDisplayElo(current);

      if (currentStep >= steps) {
        setDisplayElo(newElo);
        clearInterval(interval);
      }
    }, stepDuration);

    return () => clearInterval(interval);
  }, [animatingElo, oldElo, newElo, isPvPorAI]);

  const getResultMessage = () => {
    if (isTie) return "🤝 It's a Tie!";
    if (playerWon) return "🎉 Victory!";
    return "😔 Defeat";
  };

  const getResultColor = () => {
    if (isTie) return "from-blue-600 to-cyan-600";
    if (playerWon) return "from-green-600 to-emerald-600";
    return "from-red-600 to-rose-600";
  };

  const opponentName =
    game.game_mode === "ai"
      ? `${game.opponent_name} 🤖`
      : game.opponent_name || "Opponent";

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.8, y: 50 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full"
      >
        {/* Result Message */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className={`text-3xl sm:text-4xl font-bold text-center mb-6 bg-gradient-to-r ${getResultColor()} bg-clip-text text-transparent py-2 leading-normal`}
        >
          {getResultMessage()}
        </motion.div>

        {/* Game Summary */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="space-y-4 mb-6"
        >
          {/* If player won */}
          {playerWon && !isTie && (
            <div className="bg-green-50 rounded-lg p-4 border-2 border-green-200">
              <p className="text-sm text-green-700 mb-2">
                You cracked the code:
              </p>
              <p className="text-3xl font-mono font-bold text-green-900 text-center tracking-wider">
                {game.self_secret}
              </p>
              <p className="text-sm text-green-600 mt-2 text-center">
                in {game.self_guesses.length}{" "}
                {game.self_guesses.length === 1 ? "attempt" : "attempts"}!
              </p>
            </div>
          )}

          {/* If opponent won */}
          {opponentWon && !isTie && (
            <div className="bg-red-50 rounded-lg p-4 border-2 border-red-200">
              <p className="text-sm text-red-700 mb-2">
                {opponentName} cracked your code:
              </p>
              <p className="text-3xl font-mono font-bold text-red-900 text-center tracking-wider">
                {game.opponent_secret || "****"}
              </p>
              <p className="text-sm text-red-600 mt-2 text-center">
                in {game.opponent_guesses?.length || 0}{" "}
                {game.opponent_guesses?.length === 1 ? "attempt" : "attempts"}
              </p>
            </div>
          )}

          {/* If tie */}
          {isTie && (
            <div className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-blue-700 mb-1">
                    You both succeeded!
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-blue-600">
                      Your attempts:
                    </span>
                    <span className="font-bold text-blue-900">
                      {game.self_guesses.length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-blue-600">
                      Opponent's attempts:
                    </span>
                    <span className="font-bold text-blue-900">
                      {game.opponent_guesses?.length || 0}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </motion.div>

        {/* ELO Display - only for PvP and AI modes */}
        {isPvPorAI && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg p-6 mb-6 border-2 border-indigo-200"
          >
            <p className="text-sm text-gray-600 text-center mb-2">ELO Rating</p>

            <div className="flex items-center justify-center space-x-4">
              <div className="text-center">
                <p className="text-xs text-gray-500 mb-1">Previous</p>
                <p className="text-2xl font-bold text-gray-700">{oldElo}</p>
              </div>

              <div className="text-2xl text-gray-400">→</div>

              <div className="text-center">
                <p className="text-xs text-gray-500 mb-1">New</p>
                <motion.p
                  key={displayElo}
                  className={`text-2xl font-bold ${
                    eloChange > 0
                      ? "text-green-600"
                      : eloChange < 0
                        ? "text-red-600"
                        : "text-gray-700"
                  }`}
                >
                  {displayElo}
                </motion.p>
              </div>
            </div>

            {eloChange !== 0 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.8, duration: 0.3 }}
                className="text-center mt-3"
              >
                <span
                  className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                    eloChange > 0
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {eloChange > 0 ? "+" : ""}
                  {eloChange}
                </span>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* Exit Button */}
        <motion.button
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          onClick={onExit}
          className="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all hover:scale-105"
        >
          Back to Menu
        </motion.button>
      </motion.div>
    </div>
  );
}
