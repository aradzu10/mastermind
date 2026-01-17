import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useGameStore } from "../../store/gameStore";

interface WaitingForMatchProps {
  gameId: number;
  playerSecret: string;
  onMatchFound: () => void;
  onCancel: () => void;
  isAI?: boolean;
}

export function WaitingForMatch({
  gameId,
  playerSecret,
  onMatchFound,
  onCancel,
  isAI = false,
}: WaitingForMatchProps) {
  const { getGame, game } = useGameStore();
  const [showSecret, setShowSecret] = useState(false);
  const [revealedDigits, setRevealedDigits] = useState<number[]>([]);

  useEffect(() => {
    if (isAI) {
      // For AI, start secret animation immediately
      const timer = setTimeout(() => setShowSecret(true), 500);
      return () => clearTimeout(timer);
    } else {
      // For PvP, poll for opponent
      const pollInterval = setInterval(async () => {
        await getGame(gameId);

        // Check if opponent joined
        if (game?.status === "in_progress" && game?.opponent_id) {
          setShowSecret(true);
          clearInterval(pollInterval);
        }
      }, 5000); // Poll every 5 seconds

      return () => clearInterval(pollInterval);
    }
  }, [gameId, getGame, game?.status, game?.opponent_id, isAI]);

  // Slot machine animation - reveal digits one by one
  useEffect(() => {
    if (showSecret && revealedDigits.length < 4) {
      const timer = setTimeout(() => {
        setRevealedDigits((prev) => [...prev, prev.length]);
      }, 300); // 0.3s per digit

      return () => clearTimeout(timer);
    } else if (showSecret && revealedDigits.length === 4) {
      // All digits revealed, transition to match found
      const timer = setTimeout(onMatchFound, 500);
      return () => clearTimeout(timer);
    }
  }, [showSecret, revealedDigits, onMatchFound]);

  const SlotDigit = ({
    digit,
    index,
    revealed,
  }: {
    digit: string;
    index: number;
    revealed: boolean;
  }) => {
    const [currentNum, setCurrentNum] = useState(0);

    useEffect(() => {
      if (!revealed) {
        const interval = setInterval(() => {
          setCurrentNum((prev) => (prev + 1) % 10);
        }, 50); // Rapid cycling

        return () => clearInterval(interval);
      } else {
        setCurrentNum(parseInt(digit));
      }
    }, [revealed, digit]);

    return (
      <motion.div
        className="inline-block w-14 h-20 mx-1 bg-purple-100 rounded-lg border-2 border-purple-300 flex items-center justify-center"
        animate={revealed ? {} : { y: [0, -5, 0] }}
        transition={{ duration: 0.05, repeat: Infinity }}
      >
        <motion.span
          key={revealed ? "final" : currentNum}
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-4xl font-mono font-bold text-purple-900"
        >
          {revealed ? digit : currentNum}
        </motion.span>
      </motion.div>
    );
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center">
        {/* FIX: Changed text-4xl to text-2xl sm:text-4xl and added pb-1 */}
        <h1 className="text-2xl sm:text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent pb-1">
          {isAI ? "AI Match" : "Multiplayer Match"}
        </h1>

        {/* Animated Sword */}
        <div className="text-8xl mb-6 animate-pulse">⚔️</div>

        <AnimatePresence mode="wait">
          {!showSecret ? (
            <motion.div
              key="waiting"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <p className="text-xl text-gray-700 mb-4 font-semibold">
                {isAI ? "Preparing match..." : "Waiting for opponent..."}
              </p>

              {/* ELO display */}
              {game?.self_elo && (
                <div className="text-center mb-4">
                  <p className="text-sm text-gray-600">
                    Your ELO:{" "}
                    <span className="font-bold text-gray-800">
                      {game.self_elo}
                    </span>
                  </p>
                </div>
              )}

              <div className="flex items-center justify-center space-x-2 mb-6">
                <div
                  className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce"
                  style={{ animationDelay: "0ms" }}
                ></div>
                <div
                  className="w-3 h-3 bg-purple-600 rounded-full animate-bounce"
                  style={{ animationDelay: "150ms" }}
                ></div>
                <div
                  className="w-3 h-3 bg-pink-600 rounded-full animate-bounce"
                  style={{ animationDelay: "300ms" }}
                ></div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="secret"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mb-6"
            >
              <p className="text-xl text-gray-700 mb-4 font-semibold">
                Your Secret Code:
              </p>
              <div className="flex justify-center items-center">
                {playerSecret.split("").map((digit, index) => (
                  <SlotDigit
                    key={index}
                    digit={digit}
                    index={index}
                    revealed={revealedDigits.includes(index)}
                  />
                ))}
              </div>
              <p className="text-xs text-purple-600 mt-4">
                Your opponent will try to guess this code
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {!showSecret && (
          <button
            onClick={onCancel}
            className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
}
