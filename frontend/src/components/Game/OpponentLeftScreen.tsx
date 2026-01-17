import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Game } from "../../types/game";

interface OpponentLeftScreenProps {
  game: Game;
  onExit: () => void;
}

export function OpponentLeftScreen({ game, onExit }: OpponentLeftScreenProps) {
  const [animatingElo, setAnimatingElo] = useState(false);

  // Use the old ELO stored before game completion
  const oldElo = game.old_self_elo ?? -1;

  const [displayElo, setDisplayElo] = useState(oldElo);
  const [newElo, setNewElo] = useState(oldElo);
  const [eloChange, setEloChange] = useState(0);

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
          className="text-3xl sm:text-4xl font-bold text-center mb-6 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent py-2 leading-normal"
        >
          🚪 Opponent Left
        </motion.div>

        {/* Game Summary */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="space-y-4 mb-6"
        >
          <div className="bg-orange-50 rounded-lg p-4 border-2 border-orange-200">
            <p className="text-sm text-orange-700 mb-2 text-center">
              {opponentName} has left the game
            </p>
            <p className="text-lg font-semibold text-orange-900 text-center">
              You win by forfeit!
            </p>
          </div>

          {/* Show the codes */}
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="space-y-2">
              <div>
                <p className="text-xs text-gray-600">Your secret code:</p>
                <p className="text-xl font-mono font-bold text-gray-900 tracking-wider">
                  {game.opponent_secret}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-600">Opponent's secret code:</p>
                <p className="text-xl font-mono font-bold text-gray-900 tracking-wider">
                  {game.self_secret || "????"}
                </p>
              </div>
            </div>
          </div>
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
                  className="text-2xl font-bold text-green-600"
                >
                  {displayElo}
                </motion.p>
              </div>
            </div>

            {eloChange !== 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2.5 }}
                className="mt-4 text-center"
              >
                <span className="text-sm font-semibold text-green-600">
                  +{eloChange} ELO
                </span>
              </motion.div>
            )}
          </motion.div>
        )}

        {/* Back to Menu Button */}
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          onClick={onExit}
          className="w-full px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold
                     hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl
                     transform hover:scale-105"
        >
          Back to Menu
        </motion.button>
      </motion.div>
    </div>
  );
}
