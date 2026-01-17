import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Game } from "../../types/game";

interface MatchFoundScreenProps {
  game: Game;
  onComplete: () => void;
}

export function MatchFoundScreen({ game, onComplete }: MatchFoundScreenProps) {
  const [animationComplete, setAnimationComplete] = useState(false);

  useEffect(() => {
    if (animationComplete) {
      const timer = setTimeout(onComplete, 300);
      return () => clearTimeout(timer);
    }
  }, [animationComplete, onComplete]);

  const opponentName =
    game.game_mode === "ai"
      ? `${game.opponent_name} 🤖`
      : game.opponent_name || "Opponent";

  return (
    // Outer container: overflow-hidden here prevents the window scrollbar when swords get huge
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4 overflow-hidden">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        // Card: Removed overflow-hidden so swords can pop out visually
        className="relative bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center flex flex-col items-center"
      >
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.3 }}
          className="text-3xl font-bold mb-8 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
        >
          Match Found!
        </motion.h1>

        {/* Opponent Info */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
          className="w-full"
        >
          <p className="text-2xl font-bold text-gray-800">{opponentName}</p>
          {game.opponent_elo && (
            <p className="text-sm text-gray-600">ELO: {game.opponent_elo}</p>
          )}
        </motion.div>

        {/* Animated Swords Container
           1. relative: Keeps it in the flow (reserves space between texts).
           2. z-50: Ensures when it scales up, it covers the text/card.
           3. my-6: Adds a little breathing room.
        */}
        <div className="relative z-50 my-6">
          <motion.div
            className="text-8xl"
            initial={{ rotate: 0, scale: 1 }}
            animate={{
              rotate: [0, 360, 360, 360],
              scale: [1, 1, 3, 1],
            }}
            transition={{
              duration: 1.5,
              times: [0, 0.15, 0.85, 1],
              ease: "easeInOut",
            }}
            onAnimationComplete={() => {
              setTimeout(() => {
                setAnimationComplete(true);
              }, 500);
            }}
          >
            ⚔️
          </motion.div>
        </div>

        {/* Self Info */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
          className="w-full"
        >
          <p className="text-2xl font-bold text-gray-800">{game.self_name}</p>
          {game.self_elo && (
            <p className="text-sm text-gray-600">ELO: {game.self_elo}</p>
          )}
        </motion.div>
      </motion.div>
    </div>
  );
}
