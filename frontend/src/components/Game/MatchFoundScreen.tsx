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
      : game.opponent_name || "Yourself (no pressure)";

  const goesFirst = game.starter_id === game.self_id;
  const turnMessage = goesFirst ? "You Go First!" : "You Go Second!";
  const freeGuessMessage = goesFirst
    ? "Your opponent got a free random guess"
    : "Don't worry, you will get a free random guess";

  return (
    <div className="flex flex-col items-center justify-center min-h-screen h-screen overflow-y-scroll bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4 overflow-hidden">
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
           w-full: Takes full width of the card
           h-40: Fixed height to prevent layout shifts
           relative: allows absolute positioning inside
        */}
        <div className="relative w-full h-40">
          {/* SWORDS */}
          {/* We center the sword manually with flex inside the relative container */}
          <div className="absolute inset-0 flex items-center justify-center z-0">
            <motion.div
              className="text-8xl leading-none"
              initial={{ rotate: 0, scale: 1 }}
              animate={{
                rotate: [0, 360, 360],
                scale: [1, 1, 1, 4, 1],
              }}
              transition={{
                duration: 3,
                times: [0, 0.3, 0.5, 0.9, 1],
                ease: "easeInOut",
              }}
              onAnimationComplete={() => {
                setTimeout(() => {
                  setAnimationComplete(true);
                }, 200);
              }}
            >
              ⚔️
            </motion.div>
          </div>

          {/* BANNER 
             absolute inset-0: Stretches to fill the container
             flex items-center justify-center: Centers the content PERFECTLY
          */}
          {game.game_mode !== "single" && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5, duration: 0.4 }}
              className="absolute inset-0 z-50 flex items-center justify-center pointer-events-none"
            >
              <div className="max-w-[90%] bg-gradient-to-r from-purple-600/60 to-indigo-600/60 backdrop-blur-md text-white px-6 py-3 rounded-lg shadow-lg border border-white/20">
                <p className="text-xl font-bold text-center whitespace-nowrap">
                  {turnMessage}
                </p>
                <p className="text-xs text-center opacity-90 mt-1 font-medium">
                  {freeGuessMessage}
                </p>
              </div>
            </motion.div>
          )}
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
