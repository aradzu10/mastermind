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

  const goesFirst = game.current_turn === game.self_id;
  const turnMessage = goesFirst ? "You Go First!" : "You Go Second!";
  const freeGuessMessage = goesFirst
    ? "Your opponent got a free random guess"
    : "Don't worry, you will get a free random guess";

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4 overflow-hidden">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="relative bg-white rounded-2xl shadow-2xl p-6 max-w-md w-full text-center flex flex-col items-center"
      >
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.3 }}
          className="text-3xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
        >
          Match Found!
        </motion.h1>

        {/* Opponent Info */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
          className="w-full mb-2"
        >
          <p className="text-2xl font-bold text-gray-800">{opponentName}</p>
          {game.opponent_elo && (
            <p className="text-sm text-gray-600">ELO: {game.opponent_elo}</p>
          )}
        </motion.div>

        {/* ANIMATION CONTAINER 
            w-full: Ensures the center point is the true center of the card.
            h-40: Reserves vertical space so elements don't jump around.
        */}
        <div className="relative w-full h-40 flex items-center justify-center">
          {/* SWORDS */}
          <motion.div
            className="relative z-0 text-8xl leading-none"
            initial={{ rotate: 0, scale: 1 }}
            animate={{
              rotate: [0, 720, 720, 720],
              scale: [1, 1, 3, 1],
            }}
            transition={{
              duration: 4.5, // Total animation time (Slower)
              // [Start, Spin Start, Shrink Start, End]
              // 0 -> 0.1: Initial delay
              // 0.1 -> 0.9: Grow and Rotate (Slow)
              // 0.9 -> 1.0: Snap back to small (Fast)
              times: [0, 0.1, 0.9, 1],
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

          {/* BANNER 
             absolute top-1/2 left-1/2: Centers specifically within the w-full parent.
             bg-opacity/40: Much more transparent.
          */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="absolute z-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full px-4"
          >
            <div className="mx-auto max-w-[90%] bg-gradient-to-r from-purple-600/40 to-indigo-600/40 backdrop-blur-md text-white px-6 py-3 rounded-lg shadow-lg border border-white/10">
              <p className="text-xl font-bold text-center whitespace-nowrap">
                {turnMessage}
              </p>
              <p className="text-xs text-center opacity-90 mt-1 font-medium">
                {freeGuessMessage}
              </p>
            </div>
          </motion.div>
        </div>

        {/* Self Info */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
          className="w-full mt-2"
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
